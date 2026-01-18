"""
メインゲームループ管理モジュール（シーン管理対応）
"""

import pygame
from typing import Optional, Dict
from .settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WINDOW_TITLE,
    TARGET_FPS,
    COLOR_BACKGROUND,
)
from .input_handler import InputHandler
from .cursor import Cursor
from .profile import load_profile, apply_profile_to_input_handler


class Game:
    """メインゲームクラス"""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)
        
        # ディスプレイ設定
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # マウスカーソルを非表示に
        pygame.mouse.set_visible(False)
        
        # コンポーネント初期化
        self.input_handler = InputHandler()
        self.cursor = Cursor()
        
        # プロファイル読み込み
        profile = load_profile()
        apply_profile_to_input_handler(profile, self.input_handler)
        
        # フォント（クロスプラットフォーム対応）
        import platform
        system = platform.system()
        
        try:
            if system == "Darwin":  # macOS
                self.font = pygame.font.SysFont("hiraginosansgb", 18)
                self.font_large = pygame.font.SysFont("hiraginosansgb", 28)
            elif system == "Windows":
                # Windows標準の日本語フォント
                self.font = pygame.font.SysFont("msgothic,meiryo,yugothic", 18)
                self.font_large = pygame.font.SysFont("msgothic,meiryo,yugothic", 28)
            else:  # Linux等
                self.font = pygame.font.SysFont("notosanscjkjp,takao,ipagothic", 18)
                self.font_large = pygame.font.SysFont("notosanscjkjp,takao,ipagothic", 28)
        except:
            # フォールバック
            self.font = pygame.font.Font(None, 24)
            self.font_large = pygame.font.Font(None, 36)
        
        # 状態
        self.running = True
        self.dt = 0.0
        
        # シーン管理
        self.scenes: Dict[str, any] = {}
        self.current_scene = None
        self._init_scenes()

    def _init_scenes(self) -> None:
        """シーンを初期化"""
        from .scenes.launcher import LauncherScene
        from .scenes.tracking import TrackingScene
        from .scenes.flicking import FlickingScene
        from .scenes.stats import StatsScene
        
        self.scenes = {
            "launcher": LauncherScene(self),
            "tracking": TrackingScene(self),
            "flicking": FlickingScene(self),
            "stats": StatsScene(self),
        }
        self.current_scene = self.scenes["launcher"]
        self.current_scene.on_enter()

    def change_scene(self, scene_name: str) -> None:
        """シーンを切り替え"""
        if scene_name in self.scenes:
            if self.current_scene:
                self.current_scene.on_exit()
            self.current_scene = self.scenes[scene_name]
            self.current_scene.on_enter()
            self.current_scene.next_scene = None

    def handle_events(self) -> None:
        """イベント処理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                if self.current_scene:
                    self.current_scene.handle_event(event)

    def update(self) -> None:
        """ゲーム状態の更新"""
        if self.current_scene:
            self.current_scene.update(self.dt)
            
            # シーン遷移チェック
            if self.current_scene.next_scene:
                self.change_scene(self.current_scene.next_scene)

    def draw(self) -> None:
        """描画処理"""
        if self.current_scene:
            self.current_scene.draw(self.screen)
        
        pygame.display.flip()

    def run(self) -> None:
        """メインループ"""
        print("PyAim Cross-Platform Tracker を起動しました")
        print("ESCキーで終了します")
        
        while self.running:
            self.dt = self.clock.tick(TARGET_FPS) / 1000.0
            
            self.handle_events()
            self.update()
            self.draw()
        
        self.quit()

    def quit(self) -> None:
        """ゲーム終了処理"""
        pygame.quit()
        print("アプリケーションを終了しました")
