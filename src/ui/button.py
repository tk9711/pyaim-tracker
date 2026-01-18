"""
ボタンUIコンポーネント
"""

import pygame
from typing import Tuple, Callable, Optional


class Button:
    """クリック可能なボタン"""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        font: pygame.font.Font,
        color: Tuple[int, int, int] = (60, 60, 80),
        hover_color: Tuple[int, int, int] = (80, 80, 120),
        text_color: Tuple[int, int, int] = (255, 255, 255),
        border_radius: int = 8,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_radius = border_radius
        
        self.is_hovered = False
        self.is_pressed = False
        self.enabled = True
        
        # アニメーション
        self.scale = 1.0
        self.target_scale = 1.0

    def update(self, mouse_pos: Tuple[int, int], mouse_clicked: bool, dt: float = 0.016) -> bool:
        """
        ボタンの状態を更新
        
        Args:
            mouse_pos: マウス位置
            mouse_clicked: クリックされたか
            dt: Delta time（秒）
        
        Returns:
            True: クリックされた, False: クリックされていない
        """
        if not self.enabled:
            return False
            
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # ホバー時のスケール変更
        self.target_scale = 1.05 if self.is_hovered else 1.0
        
        # スケールアニメーション（スムーズに遷移）
        self.scale += (self.target_scale - self.scale) * 10 * dt
        
        if self.is_hovered and mouse_clicked:
            return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        """ボタンを描画"""
        # スケール適用
        if abs(self.scale - 1.0) > 0.01:
            # スケールされた矩形を計算
            scaled_width = int(self.rect.width * self.scale)
            scaled_height = int(self.rect.height * self.scale)
            scaled_x = self.rect.centerx - scaled_width // 2
            scaled_y = self.rect.centery - scaled_height // 2
            draw_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        else:
            draw_rect = self.rect
        
        # 背景色
        color = self.hover_color if self.is_hovered else self.color
        if not self.enabled:
            color = (40, 40, 50)
        
        pygame.draw.rect(surface, color, draw_rect, border_radius=self.border_radius)
        
        # 枠線
        border_color = (100, 100, 140) if self.is_hovered else (80, 80, 100)
        pygame.draw.rect(surface, border_color, draw_rect, width=2, border_radius=self.border_radius)
        
        # テキスト
        text_color = self.text_color if self.enabled else (100, 100, 100)
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=draw_rect.center)
        surface.blit(text_surface, text_rect)

    def set_position(self, x: int, y: int) -> None:
        """ボタン位置を設定"""
        self.rect.x = x
        self.rect.y = y
