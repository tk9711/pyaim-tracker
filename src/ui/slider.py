"""
スライダーUIコンポーネント
"""

import pygame
from typing import Tuple


class Slider:
    """値調整用スライダー"""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        min_value: float,
        max_value: float,
        initial_value: float,
        label: str,
        font: pygame.font.Font,
        color: Tuple[int, int, int] = (60, 60, 80),
        handle_color: Tuple[int, int, int] = (100, 200, 255),
        text_color: Tuple[int, int, int] = (255, 255, 255),
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.label = label
        self.font = font
        self.color = color
        self.handle_color = handle_color
        self.text_color = text_color
        
        self.handle_radius = height // 2 + 2
        self.dragging = False
        self.track_y = y + height // 2

    def _value_to_x(self) -> int:
        """値をX座標に変換"""
        ratio = (self.value - self.min_value) / (self.max_value - self.min_value)
        return int(self.rect.x + ratio * self.rect.width)

    def _x_to_value(self, x: int) -> float:
        """X座標を値に変換"""
        ratio = (x - self.rect.x) / self.rect.width
        ratio = max(0, min(1, ratio))
        return self.min_value + ratio * (self.max_value - self.min_value)

    def update(self, mouse_pos: Tuple[int, int], mouse_pressed: bool, mouse_just_pressed: bool) -> bool:
        """
        スライダーの状態を更新
        
        Returns:
            True: 値が変更された, False: 変更なし
        """
        handle_x = self._value_to_x()
        handle_rect = pygame.Rect(
            handle_x - self.handle_radius,
            self.track_y - self.handle_radius,
            self.handle_radius * 2,
            self.handle_radius * 2
        )
        
        # ドラッグ開始判定
        if mouse_just_pressed and handle_rect.collidepoint(mouse_pos):
            self.dragging = True
        
        # ドラッグ中
        if self.dragging:
            if mouse_pressed:
                old_value = self.value
                self.value = self._x_to_value(mouse_pos[0])
                return old_value != self.value
            else:
                self.dragging = False
        
        return False

    def draw(self, surface: pygame.Surface) -> None:
        """スライダーを描画"""
        # ラベル（整数値の場合は小数点なし）
        if self.value == int(self.value):
            label_text = f"{self.label}: {int(self.value)}"
        else:
            label_text = f"{self.label}: {self.value:.2f}"
        label_surface = self.font.render(label_text, True, self.text_color)
        surface.blit(label_surface, (self.rect.x, self.rect.y - 25))
        
        # トラック（背景）
        track_rect = pygame.Rect(self.rect.x, self.track_y - 3, self.rect.width, 6)
        pygame.draw.rect(surface, self.color, track_rect, border_radius=3)
        
        # 塗りつぶし部分
        handle_x = self._value_to_x()
        fill_rect = pygame.Rect(self.rect.x, self.track_y - 3, handle_x - self.rect.x, 6)
        pygame.draw.rect(surface, self.handle_color, fill_rect, border_radius=3)
        
        # ハンドル
        pygame.draw.circle(surface, self.handle_color, (handle_x, self.track_y), self.handle_radius)
        pygame.draw.circle(surface, (255, 255, 255), (handle_x, self.track_y), self.handle_radius - 3)

    def set_value(self, value: float) -> None:
        """値を設定"""
        self.value = max(self.min_value, min(self.max_value, value))

    def get_value(self) -> float:
        """現在の値を取得"""
        return self.value
