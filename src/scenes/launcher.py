"""
ランチャー画面
"""

import pygame
from .base import Scene
from ..ui.button import Button
from ..ui.slider import Slider
from ..profile import save_profile, create_profile_from_input_handler
from ..settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BACKGROUND, COLOR_TEXT, COLOR_ACCENT


class LauncherScene(Scene):
    """ランチャー画面 - デバイス設定とモード選択"""

    def __init__(self, game):
        super().__init__(game)
        
        self.font = game.font
        self.font_large = game.font_large
        
        # ボタン
        button_width = 200
        button_height = 50
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        
        # トレーニングモード選択ボタン
        self.tracking_button = Button(
            center_x, 250, button_width, button_height,
            "Tracking", self.font,
            color=(60, 100, 60), hover_color=(80, 140, 80)
        )
        
        self.flicking_button = Button(
            center_x, 310, button_width, button_height,
            "Flicking", self.font,
            color=(100, 60, 60), hover_color=(140, 80, 80)
        )
        
        # 下部のボタン（横並び）
        button_small_width = 95
        left_button_x = SCREEN_WIDTH // 2 - button_small_width - 5
        right_button_x = SCREEN_WIDTH // 2 + 5
        
        self.save_button = Button(
            left_button_x, 630, button_small_width, button_height,
            "保存", self.font,
            color=(60, 60, 100), hover_color=(80, 80, 140)
        )
        
        self.stats_button = Button(
            right_button_x, 630, button_small_width, button_height,
            "統計", self.font,
            color=(80, 60, 100), hover_color=(120, 80, 140)
        )
        
        # スライダー
        slider_width = 300
        slider_x = SCREEN_WIDTH // 2 - slider_width // 2
        
        # 入力設定スライダー
        self.sensitivity_slider = Slider(
            slider_x, 400, slider_width, 20,
            100, 1000, game.input_handler.gamepad_sensitivity,
            "感度", self.font
        )
        
        self.deadzone_slider = Slider(
            slider_x, 450, slider_width, 20,
            0.0, 0.3, game.input_handler.deadzone,
            "デッドゾーン", self.font
        )
        
        # トレーニング設定スライダー
        self.tracking_time_slider = Slider(
            slider_x, 510, slider_width, 20,
            10, 60, 30,
            "Tracking時間 (秒)", self.font,
            color=(60, 100, 60), handle_color=(100, 200, 100)
        )
        
        self.flicking_count_slider = Slider(
            slider_x, 570, slider_width, 20,
            5, 30, 10,
            "Flickingターゲット数", self.font,
            color=(100, 60, 60), handle_color=(255, 120, 120)
        )
        
        # マウス状態
        self._mouse_just_pressed = False
        self._mouse_was_pressed = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.running = False

    def update(self, dt: float) -> None:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        self._mouse_just_pressed = mouse_pressed and not self._mouse_was_pressed
        self._mouse_was_pressed = mouse_pressed
        
        # カーソル位置をマウス位置に同期
        self.game.cursor.set_position(mouse_pos[0], mouse_pos[1])
        
        # ボタン更新
        if self.tracking_button.update(mouse_pos, self._mouse_just_pressed):
            # Tracking設定を渡す
            tracking_scene = self.game.scenes["tracking"]
            tracking_scene.session_duration = int(self.tracking_time_slider.get_value())
            self.request_scene_change("tracking")
        
        if self.flicking_button.update(mouse_pos, self._mouse_just_pressed):
            # Flicking設定を渡す
            flicking_scene = self.game.scenes["flicking"]
            flicking_scene.target_count = int(self.flicking_count_slider.get_value())
            self.request_scene_change("flicking")
        
        if self.save_button.update(mouse_pos, self._mouse_just_pressed):
            profile = create_profile_from_input_handler(self.game.input_handler)
            if save_profile(profile):
                print("設定を保存しました")
        
        if self.stats_button.update(mouse_pos, self._mouse_just_pressed):
            self.request_scene_change("stats")
        
        # スライダー更新
        if self.sensitivity_slider.update(mouse_pos, mouse_pressed, self._mouse_just_pressed):
            self.game.input_handler.set_gamepad_sensitivity(self.sensitivity_slider.get_value())
        
        if self.deadzone_slider.update(mouse_pos, mouse_pressed, self._mouse_just_pressed):
            self.game.input_handler.set_deadzone(self.deadzone_slider.get_value())
        
        # トレーニング設定スライダー更新
        self.tracking_time_slider.update(mouse_pos, mouse_pressed, self._mouse_just_pressed)
        self.flicking_count_slider.update(mouse_pos, mouse_pressed, self._mouse_just_pressed)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(COLOR_BACKGROUND)
        
        # タイトル
        title = self.font_large.render("PyAim Tracker", True, COLOR_ACCENT)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title, title_rect)
        
        # サブタイトル
        subtitle = self.font.render("トレーニングモードを選択してください", True, COLOR_TEXT)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 130))
        surface.blit(subtitle, subtitle_rect)
        
        # デバイス情報
        device = self.game.input_handler.get_active_device()
        device_text = self.font.render(f"現在のデバイス: {device.upper()}", True, COLOR_TEXT)
        surface.blit(device_text, (SCREEN_WIDTH // 2 - 100, 180))
        
        if self.game.input_handler.is_gamepad_connected():
            status_text = self.font.render("🎮 ゲームパッド: 接続中", True, (100, 255, 150))
        else:
            status_text = self.font.render("🖱 マウスモード", True, (200, 200, 200))
        surface.blit(status_text, (SCREEN_WIDTH // 2 - 80, 210))
        
        # モード説明
        tracking_desc = self.font.render("動くターゲットを追い続ける", True, (150, 150, 150))
        surface.blit(tracking_desc, (SCREEN_WIDTH // 2 + 110, 265))
        
        flicking_desc = self.font.render("素早くターゲットを撃つ", True, (150, 150, 150))
        surface.blit(flicking_desc, (SCREEN_WIDTH // 2 + 110, 325))
        
        # ボタン描画
        self.tracking_button.draw(surface)
        self.flicking_button.draw(surface)
        self.save_button.draw(surface)
        self.stats_button.draw(surface)
        
        # スライダー描画
        self.sensitivity_slider.draw(surface)
        self.deadzone_slider.draw(surface)
        self.tracking_time_slider.draw(surface)
        self.flicking_count_slider.draw(surface)
        
        # 操作説明
        help_text = self.font.render("ESC: 終了", True, (100, 100, 100))
        surface.blit(help_text, (10, SCREEN_HEIGHT - 30))
        
        # カーソル描画
        self.game.cursor.draw(surface)
