"""
Flickingモード（瞬間エイム）
"""

import pygame
import time
from .base import Scene
from ..target import Target
from ..cursor import Cursor
from ..ui.button import Button
from ..session_logger import save_flicking_session, load_flicking_sessions
from ..effects import ParticleSystem, ScoreAnimation
from ..settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_BACKGROUND, COLOR_TEXT, COLOR_ACCENT, COLOR_SUCCESS,
    DeviceType,
)


class FlickingScene(Scene):
    """Flickingモード - 素早くターゲットを撃つ"""

    def __init__(self, game):
        super().__init__(game)
        
        self.font = game.font
        self.font_large = game.font_large
        
        # ターゲット
        self.target = Target(radius=40)
        
        # カーソル
        self.cursor = game.cursor
        
        # セッション設定
        self.target_count = 10  # ターゲット数
        self.current_target = 0
        self.session_active = False
        
        # 統計
        self.reaction_times = []
        self.target_spawn_time = 0.0
        self.hits = 0
        
        # リザルト表示
        self.show_result = False
        
        # エフェクト
        self.particles = ParticleSystem()
        self.score_animation = None
        
        # UI
        self.back_button = Button(
            10, 10, 100, 40,
            "戻る", self.font
        )
        
        self.start_button = Button(
            SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 25, 150, 50,
            "スタート", self.font,
            color=(100, 60, 60), hover_color=(140, 80, 80)
        )
        
        self.retry_button = Button(
            SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 80, 150, 50,
            "もう一度", self.font,
            color=(100, 60, 60), hover_color=(140, 80, 80)
        )
        
        # マウス状態
        self._mouse_just_pressed = False
        self._mouse_was_pressed = False
        self._click_processed = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.session_active:
                    self._end_session()
                else:
                    self.request_scene_change("launcher")

    def update(self, dt: float) -> None:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        self._mouse_just_pressed = mouse_pressed and not self._mouse_was_pressed
        self._mouse_was_pressed = mouse_pressed
        
        # 入力更新
        self.game.input_handler.update()
        
        # カーソル更新
        if self.game.input_handler.active_device == DeviceType.MOUSE:
            self.cursor.set_position(mouse_pos[0], mouse_pos[1])
        else:
            dx, dy = self.game.input_handler.get_cursor_velocity(dt)
            self.cursor.update(dx, dy)
        
        # ボタン更新
        if self.back_button.update(mouse_pos, self._mouse_just_pressed):
            self.request_scene_change("launcher")
        
        if not self.session_active and not self.show_result:
            if self.start_button.update(mouse_pos, self._mouse_just_pressed):
                self._start_session()
        
        if self.show_result:
            if self.retry_button.update(mouse_pos, self._mouse_just_pressed):
                self._reset()
        
        # セッション中 - クリックで判定
        if self.session_active and self._mouse_just_pressed and not self._click_processed:
            self._click_processed = True
            cursor_pos = self.cursor.get_position()
            
            if self.target.check_hit(cursor_pos[0], cursor_pos[1]):
                # ヒット
                reaction_time = (time.time() - self.target_spawn_time) * 1000  # ミリ秒
                self.reaction_times.append(reaction_time)
                self.hits += 1
                # ヒットエフェクト
                self.particles.emit_burst(
                    self.target.x, self.target.y,
                    count=20, color=(100, 255, 150), speed=200
                )
                self._spawn_next_target()
            else:
                # ミス - 次のターゲットへ
                self.particles.emit_burst(
                    cursor_pos[0], cursor_pos[1],
                    count=10, color=(255, 100, 100), speed=100
                )
                self._spawn_next_target()
        
        # パーティクル更新
        if self.session_active:
            self.particles.update(dt)
        
        # クリックリセット
        if not mouse_pressed:
            self._click_processed = False

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(COLOR_BACKGROUND)
        
        # 戻るボタン
        self.back_button.draw(surface)
        
        if self.session_active:
            self._draw_session(surface)
        elif self.show_result:
            self._draw_result(surface)
        else:
            self._draw_start(surface)
        
        # パーティクル描画
        self.particles.draw(surface)
        
        # カーソル描画
        self.cursor.draw(surface)

    def _draw_start(self, surface: pygame.Surface) -> None:
        """開始前の画面"""
        title = self.font_large.render("Flicking Mode", True, COLOR_ACCENT)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        surface.blit(title, title_rect)
        
        desc = self.font.render("出現するターゲットを素早くクリックしてください", True, COLOR_TEXT)
        desc_rect = desc.get_rect(center=(SCREEN_WIDTH // 2, 200))
        surface.blit(desc, desc_rect)
        
        count_text = self.font.render(f"ターゲット数: {self.target_count}", True, COLOR_TEXT)
        count_rect = count_text.get_rect(center=(SCREEN_WIDTH // 2, 240))
        surface.blit(count_text, count_rect)
        
        self.start_button.draw(surface)

    def _draw_session(self, surface: pygame.Surface) -> None:
        """セッション中の画面"""
        # ターゲット描画
        self.target.draw(surface)
        
        # 進捗
        progress_text = self.font.render(
            f"{self.current_target}/{self.target_count}", True, COLOR_TEXT
        )
        surface.blit(progress_text, (SCREEN_WIDTH - 80, 10))
        
        # ヒット数
        hit_text = self.font.render(f"Hits: {self.hits}", True, COLOR_SUCCESS)
        surface.blit(hit_text, (SCREEN_WIDTH - 80, 40))
        
        # 直近の反応速度
        if self.reaction_times:
            last_rt = self.reaction_times[-1]
            rt_color = COLOR_SUCCESS if last_rt < 300 else COLOR_TEXT
            rt_text = self.font.render(f"{last_rt:.0f}ms", True, rt_color)
            surface.blit(rt_text, (SCREEN_WIDTH // 2 - 30, 10))

    def _draw_result(self, surface: pygame.Surface) -> None:
        """リザルト画面"""
        # スコアアニメーション更新
        if self.score_animation:
            self.score_animation.update(self.game.dt)
        
        title = self.font_large.render("結果", True, COLOR_ACCENT)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title, title_rect)
        
        # 命中率（アニメーション付き）
        accuracy = (self.hits / self.target_count) * 100 if self.target_count > 0 else 0
        display_acc = self.score_animation.get_value() if self.score_animation else accuracy
        acc_color = COLOR_SUCCESS if display_acc >= 70 else (255, 150, 100)
        acc_text = self.font_large.render(f"命中率: {display_acc:.0f}%", True, acc_color)
        acc_rect = acc_text.get_rect(center=(SCREEN_WIDTH // 2, 140))
        surface.blit(acc_text, acc_rect)
        
        # 平均反応速度
        if self.reaction_times:
            avg_rt = sum(self.reaction_times) / len(self.reaction_times)
            rt_color = COLOR_SUCCESS if avg_rt < 300 else COLOR_TEXT
            rt_text = self.font.render(f"平均反応速度: {avg_rt:.0f}ms", True, rt_color)
            rt_rect = rt_text.get_rect(center=(SCREEN_WIDTH // 2, 190))
            surface.blit(rt_text, rt_rect)
            
            # 最速
            min_rt = min(self.reaction_times)
            min_text = self.font.render(f"最速: {min_rt:.0f}ms", True, COLOR_TEXT)
            min_rect = min_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
            surface.blit(min_text, min_rect)
        
        # 評価
        if accuracy >= 90 and len(self.reaction_times) > 0 and sum(self.reaction_times)/len(self.reaction_times) < 250:
            grade = "S - Amazing!"
        elif accuracy >= 70:
            grade = "A - Great!"
        elif accuracy >= 50:
            grade = "B - Good"
        else:
            grade = "C - Keep practicing"
        
        grade_text = self.font.render(grade, True, COLOR_TEXT)
        grade_rect = grade_text.get_rect(center=(SCREEN_WIDTH // 2, 260))
        surface.blit(grade_text, grade_rect)
        
        # 直近5セッションのグラフ
        sessions = load_flicking_sessions(5)
        if sessions:
            self._draw_result_graph(surface, sessions, 310)
        else:
            grade = "C - Keep practicing"
        
        grade_text = self.font.render(grade, True, COLOR_TEXT)
        grade_rect = grade_text.get_rect(center=(SCREEN_WIDTH // 2, 330))
        surface.blit(grade_text, grade_rect)
        
        self.retry_button.draw(surface)

    def _draw_result_graph(self, surface: pygame.Surface, sessions: list, y_pos: int) -> None:
        """リザルトグラフを描画"""
        graph_width = 400
        graph_height = 80
        x_pos = SCREEN_WIDTH // 2 - graph_width // 2
        
        # タイトル
        title = self.font.render("直近5セッション", True, COLOR_TEXT)
        surface.blit(title, (x_pos, y_pos - 20))
        
        # 枠
        pygame.draw.rect(surface, (60, 60, 80), (x_pos, y_pos, graph_width, graph_height), 2)
        
        if len(sessions) < 2:
            return
        
        # データ
        accuracies = [s['accuracy'] for s in sessions]
        max_val = max(accuracies) if max(accuracies) > 0 else 100
        min_val = min(accuracies) if min(accuracies) < max_val else 0
        value_range = max_val - min_val if max_val > min_val else 1
        
        # 点とライン
        points = []
        for i, acc in enumerate(accuracies):
            px = x_pos + (i / (len(accuracies) - 1)) * graph_width
            py = y_pos + graph_height - ((acc - min_val) / value_range) * graph_height
            points.append((int(px), int(py)))
        
        # ライン描画
        if len(points) >= 2:
            pygame.draw.lines(surface, (255, 100, 100), False, points, 2)
        
        # 点描画
        for point in points:
            pygame.draw.circle(surface, (255, 100, 100), point, 4)

    def _start_session(self) -> None:
        """セッション開始"""
        self.session_active = True
        self.current_target = 0
        self.hits = 0
        self.reaction_times = []
        self.show_result = False
        
        self._spawn_next_target()

    def _spawn_next_target(self) -> None:
        """次のターゲットを出現"""
        self.current_target += 1
        
        if self.current_target > self.target_count:
            self._end_session()
            return
        
        self.target.spawn_random()
        self.target_spawn_time = time.time()

    def _end_session(self) -> None:
        """セッション終了"""
        self.session_active = False
        self.show_result = True
        self.target.is_active = False
        
        # セッション結果を保存
        accuracy = (self.hits / self.target_count) * 100 if self.target_count > 0 else 0
        avg_reaction = sum(self.reaction_times) / len(self.reaction_times) if self.reaction_times else 0
        min_reaction = min(self.reaction_times) if self.reaction_times else 0
        
        # スコアアニメーション開始
        self.score_animation = ScoreAnimation(accuracy, duration=1.5)
        
        save_flicking_session(accuracy, avg_reaction, min_reaction, self.hits, self.target_count)
        print(f"Flicking結果を保存: 命中率 {accuracy:.0f}%, 平均 {avg_reaction:.0f}ms")

    def _reset(self) -> None:
        """リセット"""
        self.session_active = False
        self.show_result = False
        self.current_target = 0
        self.hits = 0
        self.reaction_times = []
