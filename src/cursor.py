"""
カーソル（レティクル）管理モジュール
"""

import pygame
from typing import Tuple
from .settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CURSOR_SIZE,
    CURSOR_COLOR,
    CURSOR_CENTER_DOT_SIZE,
    CURSOR_CENTER_DOT_COLOR,
)


class Cursor:
    """画面上のカーソル（レティクル）を管理するクラス"""

    def __init__(self, x: float = None, y: float = None):
        """
        Args:
            x: 初期X座標（Noneの場合は画面中央）
            y: 初期Y座標（Noneの場合は画面中央）
        """
        self.x = x if x is not None else SCREEN_WIDTH / 2
        self.y = y if y is not None else SCREEN_HEIGHT / 2
        
        self.size = CURSOR_SIZE
        self.color = CURSOR_COLOR
        self.center_dot_size = CURSOR_CENTER_DOT_SIZE
        self.center_dot_color = CURSOR_CENTER_DOT_COLOR
        
        # レティクルの線の太さ
        self.line_width = 2
        self.gap = 6  # 中心からのギャップ

    def update(self, dx: float, dy: float) -> None:
        """
        カーソル位置を更新
        
        Args:
            dx: X方向の移動量
            dy: Y方向の移動量
        """
        self.x += dx
        self.y += dy
        
        # 画面境界内に制限
        self.x = max(0, min(SCREEN_WIDTH, self.x))
        self.y = max(0, min(SCREEN_HEIGHT, self.y))

    def set_position(self, x: float, y: float) -> None:
        """カーソル位置を直接設定"""
        self.x = max(0, min(SCREEN_WIDTH, x))
        self.y = max(0, min(SCREEN_HEIGHT, y))

    def get_position(self) -> Tuple[float, float]:
        """現在のカーソル位置を取得"""
        return (self.x, self.y)

    def get_center(self) -> Tuple[int, int]:
        """カーソル中心位置を整数で取得"""
        return (int(self.x), int(self.y))

    def draw(self, surface: pygame.Surface) -> None:
        """
        カーソルを描画（クロスヘア形式）
        
        Args:
            surface: 描画対象のサーフェス
        """
        cx, cy = self.get_center()
        half_size = self.size // 2
        
        # 上の線
        pygame.draw.line(
            surface,
            self.color,
            (cx, cy - half_size),
            (cx, cy - self.gap),
            self.line_width
        )
        
        # 下の線
        pygame.draw.line(
            surface,
            self.color,
            (cx, cy + self.gap),
            (cx, cy + half_size),
            self.line_width
        )
        
        # 左の線
        pygame.draw.line(
            surface,
            self.color,
            (cx - half_size, cy),
            (cx - self.gap, cy),
            self.line_width
        )
        
        # 右の線
        pygame.draw.line(
            surface,
            self.color,
            (cx + self.gap, cy),
            (cx + half_size, cy),
            self.line_width
        )
        
        # 中心のドット（ゲームパッドユーザー向け）
        pygame.draw.circle(
            surface,
            self.center_dot_color,
            (cx, cy),
            self.center_dot_size
        )

    def check_collision(self, target_x: float, target_y: float, target_radius: float) -> bool:
        """
        ターゲットとの当たり判定
        
        Args:
            target_x: ターゲットのX座標
            target_y: ターゲットのY座標
            target_radius: ターゲットの半径
            
        Returns:
            True: 衝突している, False: 衝突していない
        """
        distance = ((self.x - target_x) ** 2 + (self.y - target_y) ** 2) ** 0.5
        return distance <= target_radius
