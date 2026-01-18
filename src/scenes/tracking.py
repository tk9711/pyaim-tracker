"""
Trackingモード（追いエイム）
"""

import pygame
import time
from .base import Scene
from ..target import Target
from ..cursor import Cursor
from ..ui.button import Button
from ..session_logger import save_tracking_session, load_tracking_sessions
from ..effects import ParticleSystem, ScoreAnimation
from ..settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_BACKGROUND, COLOR_TEXT, COLOR_ACCENT, COLOR_SUCCESS,
    DeviceType,
)


class TrackingScene(Scene):
    """Trackingモード - 動くターゲットを追い続ける"""

    def __init__(self, game):
        super().__init__(game)
        
        self.font = game.font
        self.font_large = game.font_large
        
        # ターゲット
        self.target = Target(radius=50)
        self.target.spawn_random()
        self.target.set_random_velocity()
        
        # カーソル
        self.cursor = game.cursor
        
        # セッション設定
        self.session_duration = 30.0  # 秒
        self.session_start_time = 0.0
        self.session_active = False
        
        # 統計
        self.time_on_target = 0.0
        self.total_time = 0.0
        
        # リザルト表示
        self.show_result = False
        self.result_t0_rate = 0.0
        
        # エフェクト
        self.particles = ParticleSystem()
        self.score_animation = None
        self.was_on_target = False
        
        # UI
        self.back_button = Button(
            10, 10, 100, 40,
            "戻る", self.font
        )
        
        self.start_button = Button(
            SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 25, 150, 50,
            "スタート", self.font,
            color=(60, 120, 60), hover_color=(80, 160, 80)
        )
        
        self.retry_button = Button(
            SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 50, 150, 50,
            "もう一度", self.font,
            color=(60, 120, 60), hover_color=(80, 160, 80)
        )
        
        # マウス状態
        self._mouse_just_pressed = False
        self._mouse_was_pressed = False

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
        
        # セッション中
        if self.session_active:
            self.target.update(dt)
            
            # T0計測
            cursor_pos = self.cursor.get_position()
            is_on_target = self.target.check_hit(cursor_pos[0], cursor_pos[1])
            
            if is_on_target:
                self.time_on_target += dt
                # ヒット時のパーティクル（連続ヒット中は少なめに）
                if not self.was_on_target:
                    self.particles.emit_burst(
                        self.target.x, self.target.y,
                        count=15, color=(100, 255, 150), speed=150
                    )
            
            self.was_on_target = is_on_target
            self.total_time += dt
            
            # パーティクル更新
            self.particles.update(dt)
            
            # セッション終了判定
            elapsed = time.time() - self.session_start_time
            if elapsed >= self.session_duration:
                self._end_session()

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
        
        # カーソル描画（常に最前面）
        self.cursor.draw(surface)

    def _draw_start(self, surface: pygame.Surface) -> None:
        """開始前の画面"""
        title = self.font_large.render("Tracking Mode", True, COLOR_ACCENT)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        surface.blit(title, title_rect)
        
        desc = self.font.render("動くターゲットにカーソルを合わせ続けてください", True, COLOR_TEXT)
        desc_rect = desc.get_rect(center=(SCREEN_WIDTH // 2, 200))
        surface.blit(desc, desc_rect)
        
        time_text = self.font.render(f"制限時間: {self.session_duration:.0f}秒", True, COLOR_TEXT)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 240))
        surface.blit(time_text, time_rect)
        
        self.start_button.draw(surface)

    def _draw_session(self, surface: pygame.Surface) -> None:
        """セッション中の画面"""
        # ターゲット描画
        self.target.draw(surface)
        
        # 残り時間
        elapsed = time.time() - self.session_start_time
        remaining = max(0, self.session_duration - elapsed)
        time_text = self.font_large.render(f"{remaining:.1f}s", True, COLOR_TEXT)
        surface.blit(time_text, (SCREEN_WIDTH - 100, 10))
        
        # リアルタイムT0率
        if self.total_time > 0:
            current_t0 = (self.time_on_target / self.total_time) * 100
            t0_color = COLOR_SUCCESS if current_t0 >= 50 else COLOR_TEXT
            t0_text = self.font.render(f"T0: {current_t0:.1f}%", True, t0_color)
            surface.blit(t0_text, (SCREEN_WIDTH - 100, 50))
        
        # オンターゲット表示
        cursor_pos = self.cursor.get_position()
        if self.target.check_hit(cursor_pos[0], cursor_pos[1]):
            hit_text = self.font.render("ON TARGET", True, COLOR_SUCCESS)
            surface.blit(hit_text, (SCREEN_WIDTH // 2 - 50, 10))

    def _draw_result(self, surface: pygame.Surface) -> None:
        """リザルト画面"""
        # スコアアニメーション更新
        if self.score_animation:
            self.score_animation.update(self.game.dt)
        
        title = self.font_large.render("結果", True, COLOR_ACCENT)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        surface.blit(title, title_rect)
        
        # T0率（アニメーション付き）
        display_t0 = self.score_animation.get_value() if self.score_animation else self.result_t0_rate
        t0_color = COLOR_SUCCESS if display_t0 >= 50 else (255, 150, 100)
        t0_text = self.font_large.render(f"T0率: {display_t0:.1f}%", True, t0_color)
        t0_rect = t0_text.get_rect(center=(SCREEN_WIDTH // 2, 170))
        surface.blit(t0_text, t0_rect)
        
        # 評価
        if self.result_t0_rate >= 80:
            grade = "S - Excellent!"
        elif self.result_t0_rate >= 60:
            grade = "A - Great!"
        elif self.result_t0_rate >= 40:
            grade = "B - Good"
        else:
            grade = "C - Keep practicing"
        
        grade_text = self.font.render(grade, True, COLOR_TEXT)
        grade_rect = grade_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
        surface.blit(grade_text, grade_rect)
        
        # 直近5セッションのグラフ
        sessions = load_tracking_sessions(5)
        if sessions:
            self._draw_result_graph(surface, sessions, 280)
        
        self.retry_button.draw(surface)

    def _draw_result_graph(self, surface: pygame.Surface, sessions: list, y_pos: int) -> None:
        """リザルトグラフを描画"""
        graph_width = 400
        graph_height = 100
        x_pos = SCREEN_WIDTH // 2 - graph_width // 2
        
        # タイトル
        title = self.font.render("直近5セッション", True, COLOR_TEXT)
        surface.blit(title, (x_pos, y_pos - 25))
        
        # 枠
        pygame.draw.rect(surface, (60, 60, 80), (x_pos, y_pos, graph_width, graph_height), 2)
        
        if len(sessions) < 2:
            return
        
        # データ
        t0_rates = [s['t0_rate'] for s in sessions]
        max_val = max(t0_rates) if max(t0_rates) > 0 else 100
        min_val = min(t0_rates) if min(t0_rates) < max_val else 0
        value_range = max_val - min_val if max_val > min_val else 1
        
        # 点とライン
        points = []
        for i, t0 in enumerate(t0_rates):
            px = x_pos + (i / (len(t0_rates) - 1)) * graph_width
            py = y_pos + graph_height - ((t0 - min_val) / value_range) * graph_height
            points.append((int(px), int(py)))
        
        # ライン描画
        if len(points) >= 2:
            pygame.draw.lines(surface, (100, 255, 150), False, points, 2)
        
        # 点描画
        for point in points:
            pygame.draw.circle(surface, (100, 255, 150), point, 4)

    def _start_session(self) -> None:
        """セッション開始"""
        self.session_active = True
        self.session_start_time = time.time()
        self.time_on_target = 0.0
        self.total_time = 0.0
        self.show_result = False
        
        self.target.spawn_random()
        self.target.set_random_velocity()

    def _end_session(self) -> None:
        """セッション終了"""
        self.session_active = False
        self.show_result = True
        
        if self.total_time > 0:
            self.result_t0_rate = (self.time_on_target / self.total_time) * 100
        else:
            self.result_t0_rate = 0.0
        
        # スコアアニメーション開始
        self.score_animation = ScoreAnimation(self.result_t0_rate, duration=1.5)
        
        # セッション結果を保存
        save_tracking_session(self.result_t0_rate, self.session_duration)
        print(f"Tracking結果を保存: T0率 {self.result_t0_rate:.1f}%")

    def _reset(self) -> None:
        """リセット"""
        self.session_active = False
        self.show_result = False
        self.time_on_target = 0.0
        self.total_time = 0.0
