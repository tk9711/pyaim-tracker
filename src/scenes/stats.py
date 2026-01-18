"""
統計・分析ダッシュボード画面
"""

import pygame
from .base import Scene
from ..ui.button import Button
from ..session_logger import (
    get_tracking_stats,
    get_flicking_stats,
    load_tracking_sessions,
    load_flicking_sessions
)
from ..settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_BACKGROUND, COLOR_TEXT, COLOR_ACCENT, COLOR_SUCCESS
)


class StatsScene(Scene):
    """統計・分析ダッシュボード"""

    def __init__(self, game):
        super().__init__(game)
        
        self.font = game.font
        self.font_large = game.font_large
        
        # ボタン
        self.back_button = Button(
            10, 10, 100, 40,
            "戻る", self.font
        )
        
        # 統計データ
        self.tracking_stats = {}
        self.flicking_stats = {}
        
        # マウス状態
        self._mouse_just_pressed = False
        self._mouse_was_pressed = False

    def on_enter(self) -> None:
        """シーン開始時にデータ読み込み"""
        self.tracking_stats = get_tracking_stats()
        self.flicking_stats = get_flicking_stats()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.request_scene_change("launcher")

    def update(self, dt: float) -> None:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        self._mouse_just_pressed = mouse_pressed and not self._mouse_was_pressed
        self._mouse_was_pressed = mouse_pressed
        
        # カーソル位置更新
        self.game.cursor.set_position(mouse_pos[0], mouse_pos[1])
        
        # ボタン更新
        if self.back_button.update(mouse_pos, self._mouse_just_pressed):
            self.request_scene_change("launcher")

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(COLOR_BACKGROUND)
        
        # 戻るボタン
        self.back_button.draw(surface)
        
        # タイトル
        title = self.font_large.render("統計・分析", True, COLOR_ACCENT)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        surface.blit(title, title_rect)
        
        # 2列レイアウト
        left_x = 100
        right_x = SCREEN_WIDTH // 2 + 50
        y_start = 120
        
        # Tracking統計
        self._draw_tracking_stats(surface, left_x, y_start)
        
        # Flicking統計
        self._draw_flicking_stats(surface, right_x, y_start)
        
        # グラフ
        self._draw_graphs(surface, y_start + 250)
        
        # カーソル描画
        self.game.cursor.draw(surface)

    def _draw_tracking_stats(self, surface: pygame.Surface, x: int, y: int) -> None:
        """Tracking統計を描画"""
        # タイトル
        title = self.font.render("Tracking Mode", True, COLOR_ACCENT)
        surface.blit(title, (x, y))
        y += 40
        
        if self.tracking_stats['count'] == 0:
            no_data = self.font.render("データなし", True, (150, 150, 150))
            surface.blit(no_data, (x, y))
            return
        
        # セッション数
        count_text = self.font.render(
            f"セッション数: {self.tracking_stats['count']}", True, COLOR_TEXT
        )
        surface.blit(count_text, (x, y))
        y += 30
        
        # 平均T0率
        avg_text = self.font.render(
            f"平均T0率: {self.tracking_stats['avg']:.1f}%", True, COLOR_TEXT
        )
        surface.blit(avg_text, (x, y))
        y += 30
        
        # 最高T0率
        best_color = COLOR_SUCCESS if self.tracking_stats['best'] >= 70 else COLOR_TEXT
        best_text = self.font.render(
            f"最高T0率: {self.tracking_stats['best']:.1f}%", True, best_color
        )
        surface.blit(best_text, (x, y))

    def _draw_flicking_stats(self, surface: pygame.Surface, x: int, y: int) -> None:
        """Flicking統計を描画"""
        # タイトル
        title = self.font.render("Flicking Mode", True, COLOR_ACCENT)
        surface.blit(title, (x, y))
        y += 40
        
        if self.flicking_stats['count'] == 0:
            no_data = self.font.render("データなし", True, (150, 150, 150))
            surface.blit(no_data, (x, y))
            return
        
        # セッション数
        count_text = self.font.render(
            f"セッション数: {self.flicking_stats['count']}", True, COLOR_TEXT
        )
        surface.blit(count_text, (x, y))
        y += 30
        
        # 平均命中率
        avg_text = self.font.render(
            f"平均命中率: {self.flicking_stats['avg_acc']:.1f}%", True, COLOR_TEXT
        )
        surface.blit(avg_text, (x, y))
        y += 30
        
        # 最高命中率
        best_color = COLOR_SUCCESS if self.flicking_stats['best_acc'] >= 80 else COLOR_TEXT
        best_text = self.font.render(
            f"最高命中率: {self.flicking_stats['best_acc']:.1f}%", True, best_color
        )
        surface.blit(best_text, (x, y))
        y += 30
        
        # 平均反応速度
        if self.flicking_stats['avg_reaction'] > 0:
            reaction_text = self.font.render(
                f"平均反応速度: {self.flicking_stats['avg_reaction']:.0f}ms", True, COLOR_TEXT
            )
            surface.blit(reaction_text, (x, y))

    def _draw_graphs(self, surface: pygame.Surface, y_start: int) -> None:
        """スコア推移グラフを描画"""
        graph_height = 120
        graph_width = 500
        center_x = SCREEN_WIDTH // 2
        
        # Trackingグラフ
        if self.tracking_stats['count'] > 0 and self.tracking_stats['recent']:
            self._draw_line_graph(
                surface,
                center_x - graph_width // 2,
                y_start,
                graph_width,
                graph_height,
                self.tracking_stats['recent'],
                "Tracking - 直近10セッション",
                (80, 140, 80)
            )

    def _draw_line_graph(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        data: list,
        title: str,
        color: tuple
    ) -> None:
        """折れ線グラフを描画"""
        if not data:
            return
        
        # タイトル
        title_text = self.font.render(title, True, COLOR_TEXT)
        surface.blit(title_text, (x, y - 25))
        
        # 枠
        pygame.draw.rect(surface, (60, 60, 80), (x, y, width, height), 2)
        
        # データ点
        if len(data) < 2:
            return
        
        max_val = max(data) if max(data) > 0 else 100
        min_val = min(data) if min(data) < max_val else 0
        value_range = max_val - min_val if max_val > min_val else 1
        
        points = []
        for i, value in enumerate(data):
            px = x + (i / (len(data) - 1)) * width
            py = y + height - ((value - min_val) / value_range) * height
            points.append((int(px), int(py)))
        
        # 線を描画
        if len(points) >= 2:
            pygame.draw.lines(surface, color, False, points, 2)
        
        # 点を描画
        for point in points:
            pygame.draw.circle(surface, color, point, 4)
        
        # 最大値・最小値ラベル
        max_label = self.font.render(f"{max_val:.0f}", True, (150, 150, 150))
        surface.blit(max_label, (x - 40, y))
        
        min_label = self.font.render(f"{min_val:.0f}", True, (150, 150, 150))
        surface.blit(min_label, (x - 40, y + height - 15))
