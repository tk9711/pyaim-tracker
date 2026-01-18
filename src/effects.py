"""
パーティクルエフェクトシステム
"""

import pygame
import random
import math
from typing import List, Tuple


class Particle:
    """単一パーティクル"""

    def __init__(
        self,
        x: float,
        y: float,
        velocity_x: float,
        velocity_y: float,
        color: Tuple[int, int, int],
        lifetime: float,
        size: float = 4
    ):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.alpha = 255

    def update(self, dt: float) -> bool:
        """
        パーティクルを更新
        
        Returns:
            True: 生存, False: 消滅
        """
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # 重力
        self.velocity_y += 300 * dt
        
        # 寿命減少
        self.lifetime -= dt
        
        # アルファ値計算
        self.alpha = int(255 * (self.lifetime / self.max_lifetime))
        
        return self.lifetime > 0

    def draw(self, surface: pygame.Surface) -> None:
        """パーティクルを描画"""
        if self.alpha <= 0:
            return
        
        # アルファ対応の色
        color_with_alpha = (*self.color, self.alpha)
        
        # 一時サーフェスを作成してアルファブレンド
        temp_surface = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(
            temp_surface,
            color_with_alpha,
            (int(self.size), int(self.size)),
            int(self.size)
        )
        surface.blit(temp_surface, (int(self.x - self.size), int(self.y - self.size)))


class ParticleSystem:
    """パーティクルシステム管理"""

    def __init__(self):
        self.particles: List[Particle] = []

    def emit_burst(
        self,
        x: float,
        y: float,
        count: int = 20,
        color: Tuple[int, int, int] = (100, 255, 150),
        speed: float = 200.0
    ) -> None:
        """
        バースト（爆発）エフェクトを発生
        
        Args:
            x, y: 発生位置
            count: パーティクル数
            color: 色
            speed: 速度
        """
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            velocity = random.uniform(speed * 0.5, speed)
            
            particle = Particle(
                x, y,
                math.cos(angle) * velocity,
                math.sin(angle) * velocity,
                color,
                lifetime=random.uniform(0.3, 0.6),
                size=random.uniform(2, 5)
            )
            self.particles.append(particle)

    def emit_trail(
        self,
        x: float,
        y: float,
        color: Tuple[int, int, int] = (255, 100, 100),
        count: int = 3
    ) -> None:
        """
        トレイル（軌跡）エフェクトを発生
        
        Args:
            x, y: 発生位置
            color: 色
            count: パーティクル数
        """
        for _ in range(count):
            particle = Particle(
                x + random.uniform(-2, 2),
                y + random.uniform(-2, 2),
                random.uniform(-20, 20),
                random.uniform(-20, 20),
                color,
                lifetime=0.2,
                size=2
            )
            self.particles.append(particle)

    def update(self, dt: float) -> None:
        """全パーティクルを更新"""
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surface: pygame.Surface) -> None:
        """全パーティクルを描画"""
        for particle in self.particles:
            particle.draw(surface)

    def clear(self) -> None:
        """全パーティクルをクリア"""
        self.particles.clear()


class ScoreAnimation:
    """スコアカウントアップアニメーション"""

    def __init__(self, target_value: float, duration: float = 1.0):
        self.target_value = target_value
        self.current_value = 0.0
        self.duration = duration
        self.elapsed = 0.0
        self.completed = False

    def update(self, dt: float) -> None:
        """アニメーション更新"""
        if self.completed:
            return
        
        self.elapsed += dt
        
        if self.elapsed >= self.duration:
            self.current_value = self.target_value
            self.completed = True
        else:
            # イージング（ease-out）
            progress = self.elapsed / self.duration
            eased = 1 - (1 - progress) ** 3
            self.current_value = self.target_value * eased

    def get_value(self) -> float:
        """現在の値を取得"""
        return self.current_value

    def is_completed(self) -> bool:
        """アニメーション完了判定"""
        return self.completed
