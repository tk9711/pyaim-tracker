"""
ターゲットクラスモジュール
"""

import pygame
import random
import math
from typing import Tuple
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Target:
    """トレーニング用ターゲット"""

    def __init__(
        self,
        x: float = None,
        y: float = None,
        radius: float = 40,
        color: Tuple[int, int, int] = (255, 100, 100),
        outline_color: Tuple[int, int, int] = (255, 200, 200),
    ):
        self.x = x if x is not None else SCREEN_WIDTH / 2
        self.y = y if y is not None else SCREEN_HEIGHT / 2
        self.radius = radius
        self.color = color
        self.outline_color = outline_color
        
        # 移動用（Trackingモード）
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.speed = 200.0  # ピクセル/秒
        
        # ランダム要素
        self.direction_change_timer = 0.0
        self.direction_change_interval = random.uniform(1.5, 3.0)  # 方向転換間隔
        self.speed_variation_timer = 0.0
        self.speed_variation_interval = random.uniform(0.5, 1.5)  # 速度変化間隔
        self.base_speed = 200.0
        
        # 状態
        self.is_active = True
        self.hit_time = 0.0

    def spawn_random(self, margin: int = 100) -> None:
        """ランダムな位置に出現"""
        self.x = random.uniform(margin, SCREEN_WIDTH - margin)
        self.y = random.uniform(margin, SCREEN_HEIGHT - margin)
        self.is_active = True

    def set_random_velocity(self) -> None:
        """ランダムな方向に移動開始"""
        angle = random.uniform(0, 2 * math.pi)
        self.velocity_x = math.cos(angle) * self.speed
        self.velocity_y = math.sin(angle) * self.speed

    def update(self, dt: float) -> None:
        """ターゲットを更新"""
        if not self.is_active:
            return
        
        # ランダムな方向転換
        self.direction_change_timer += dt
        if self.direction_change_timer >= self.direction_change_interval:
            self.direction_change_timer = 0.0
            self.direction_change_interval = random.uniform(1.5, 3.5)
            
            # 新しい方向をランダムに設定（現在の方向から±45〜135度）
            current_angle = math.atan2(self.velocity_y, self.velocity_x)
            angle_change = random.uniform(math.pi / 4, 3 * math.pi / 4)
            if random.random() < 0.5:
                angle_change = -angle_change
            
            new_angle = current_angle + angle_change
            current_speed = math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)
            self.velocity_x = math.cos(new_angle) * current_speed
            self.velocity_y = math.sin(new_angle) * current_speed
        
        # ランダムな速度変化
        self.speed_variation_timer += dt
        if self.speed_variation_timer >= self.speed_variation_interval:
            self.speed_variation_timer = 0.0
            self.speed_variation_interval = random.uniform(0.5, 1.5)
            
            # 速度を70%〜130%の範囲でランダムに変化
            speed_multiplier = random.uniform(0.7, 1.3)
            target_speed = self.base_speed * speed_multiplier
            
            # 現在の方向を維持したまま速度を変更
            current_speed = math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)
            if current_speed > 0:
                self.velocity_x = (self.velocity_x / current_speed) * target_speed
                self.velocity_y = (self.velocity_y / current_speed) * target_speed
        
        # 移動
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # 画面端で反射
        margin = self.radius + 50
        if self.x < margin or self.x > SCREEN_WIDTH - margin:
            self.velocity_x *= -1
            self.x = max(margin, min(SCREEN_WIDTH - margin, self.x))
            # 反射時に方向転換タイマーをリセット
            self.direction_change_timer = 0.0
            self.direction_change_interval = random.uniform(1.0, 2.5)
        if self.y < margin or self.y > SCREEN_HEIGHT - margin:
            self.velocity_y *= -1
            self.y = max(margin, min(SCREEN_HEIGHT - margin, self.y))
            # 反射時に方向転換タイマーをリセット
            self.direction_change_timer = 0.0
            self.direction_change_interval = random.uniform(1.0, 2.5)

    def draw(self, surface: pygame.Surface) -> None:
        """ターゲットを描画"""
        if not self.is_active:
            return
        
        cx, cy = int(self.x), int(self.y)
        
        # 外側の円（アウトライン）
        pygame.draw.circle(surface, self.outline_color, (cx, cy), int(self.radius))
        
        # 内側の円
        pygame.draw.circle(surface, self.color, (cx, cy), int(self.radius * 0.7))
        
        # 中心のドット
        pygame.draw.circle(surface, (255, 255, 255), (cx, cy), int(self.radius * 0.2))

    def check_hit(self, cursor_x: float, cursor_y: float) -> bool:
        """カーソルとの当たり判定"""
        distance = math.sqrt((self.x - cursor_x) ** 2 + (self.y - cursor_y) ** 2)
        return distance <= self.radius

    def get_distance(self, cursor_x: float, cursor_y: float) -> float:
        """カーソルとの距離を取得"""
        return math.sqrt((self.x - cursor_x) ** 2 + (self.y - cursor_y) ** 2)

    def set_speed(self, speed: float) -> None:
        """移動速度を設定"""
        self.speed = speed
        self.base_speed = speed
        # 現在の速度ベクトルを正規化して新しい速度を適用
        current_speed = math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)
        if current_speed > 0:
            self.velocity_x = (self.velocity_x / current_speed) * speed
            self.velocity_y = (self.velocity_y / current_speed) * speed
