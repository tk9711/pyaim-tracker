"""
シーン基底クラス
"""

import pygame
from abc import ABC, abstractmethod
from typing import Optional


class Scene(ABC):
    """シーンの基底クラス"""

    def __init__(self, game):
        self.game = game
        self.next_scene: Optional[str] = None

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """イベント処理"""
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """更新処理"""
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """描画処理"""
        pass

    def on_enter(self) -> None:
        """シーン開始時に呼ばれる"""
        pass

    def on_exit(self) -> None:
        """シーン終了時に呼ばれる"""
        pass

    def request_scene_change(self, scene_name: str) -> None:
        """シーン遷移をリクエスト"""
        self.next_scene = scene_name
