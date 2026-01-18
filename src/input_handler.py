"""
入力処理モジュール - マウスとゲームパッドの統合管理
"""

import pygame
import numpy as np
from typing import Tuple, Optional
from .settings import (
    MOUSE_SENSITIVITY,
    GAMEPAD_SENSITIVITY,
    GAMEPAD_DEADZONE,
    GAMEPAD_RESPONSE_CURVE,
    DeviceType,
)


class InputHandler:
    """マウスとゲームパッドの入力を統合管理するクラス"""

    def __init__(self):
        self.joystick: Optional[pygame.joystick.JoystickType] = None
        self.active_device = DeviceType.MOUSE
        
        # マウス設定
        self.mouse_sensitivity = MOUSE_SENSITIVITY
        
        # ゲームパッド設定
        self.gamepad_sensitivity = GAMEPAD_SENSITIVITY
        self.deadzone = GAMEPAD_DEADZONE
        self.response_curve = GAMEPAD_RESPONSE_CURVE
        
        # 入力状態
        self._last_mouse_pos = (0, 0)
        self._mouse_delta = (0, 0)
        self._gamepad_axis = (0.0, 0.0)
        
        self._init_joystick()

    def _init_joystick(self) -> None:
        """ゲームパッドを初期化"""
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"ゲームパッド検出: {self.joystick.get_name()}")
        else:
            print("ゲームパッドが接続されていません。マウスモードで動作します。")

    def apply_deadzone(self, value: float) -> float:
        """
        デッドゾーンと反応曲線を適用
        
        計算式: v_output = sign(v_input) * ((max(0, |v_input| - d) / (1 - d)) ^ n) * s
        """
        if abs(value) < self.deadzone:
            return 0.0
        
        sign = 1.0 if value >= 0 else -1.0
        normalized = (abs(value) - self.deadzone) / (1.0 - self.deadzone)
        
        # 反応曲線を適用
        curved = normalized ** self.response_curve
        
        return sign * curved

    def update(self) -> None:
        """入力状態を更新（毎フレーム呼び出し）"""
        # マウスの相対移動を取得
        current_mouse_pos = pygame.mouse.get_pos()
        self._mouse_delta = (
            current_mouse_pos[0] - self._last_mouse_pos[0],
            current_mouse_pos[1] - self._last_mouse_pos[1],
        )
        self._last_mouse_pos = current_mouse_pos
        
        # マウスが動いたらマウスモードに切り替え
        if abs(self._mouse_delta[0]) > 0 or abs(self._mouse_delta[1]) > 0:
            self.active_device = DeviceType.MOUSE
        
        # ゲームパッドの軸入力を取得
        if self.joystick:
            raw_x = self.joystick.get_axis(0)  # 左スティック X軸
            raw_y = self.joystick.get_axis(1)  # 左スティック Y軸
            
            # デッドゾーン適用
            self._gamepad_axis = (
                self.apply_deadzone(raw_x),
                self.apply_deadzone(raw_y),
            )
            
            # パッドが動いたらパッドモードに切り替え
            if abs(self._gamepad_axis[0]) > 0.01 or abs(self._gamepad_axis[1]) > 0.01:
                self.active_device = DeviceType.GAMEPAD

    def get_cursor_velocity(self, dt: float) -> Tuple[float, float]:
        """
        カーソルの移動量を取得
        
        Args:
            dt: Delta time（秒）
            
        Returns:
            (dx, dy) の移動量
        """
        if self.active_device == DeviceType.MOUSE:
            # マウスの場合は相対移動に感度を適用
            return (
                self._mouse_delta[0] * self.mouse_sensitivity,
                self._mouse_delta[1] * self.mouse_sensitivity,
            )
        else:
            # ゲームパッドの場合は速度ベースで移動
            return (
                self._gamepad_axis[0] * self.gamepad_sensitivity * dt,
                self._gamepad_axis[1] * self.gamepad_sensitivity * dt,
            )

    def get_mouse_position(self) -> Tuple[int, int]:
        """現在のマウス位置を取得"""
        return pygame.mouse.get_pos()

    def get_active_device(self) -> str:
        """現在アクティブなデバイスタイプを取得"""
        return self.active_device

    def is_gamepad_connected(self) -> bool:
        """ゲームパッドが接続されているか"""
        return self.joystick is not None

    def set_deadzone(self, value: float) -> None:
        """デッドゾーンを設定（0.0 - 0.3）"""
        self.deadzone = max(0.0, min(0.3, value))

    def set_response_curve(self, value: float) -> None:
        """反応曲線の指数を設定（1.0 - 3.0）"""
        self.response_curve = max(1.0, min(3.0, value))

    def set_gamepad_sensitivity(self, value: float) -> None:
        """ゲームパッド感度を設定"""
        self.gamepad_sensitivity = max(100.0, min(1500.0, value))

    def set_mouse_sensitivity(self, value: float) -> None:
        """マウス感度を設定"""
        self.mouse_sensitivity = max(0.1, min(5.0, value))
