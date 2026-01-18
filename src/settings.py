"""
設定・定数管理モジュール
"""

# ウィンドウ設定
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WINDOW_TITLE = "PyAim Cross-Platform Tracker"
TARGET_FPS = 144

# カーソル設定
CURSOR_SIZE = 24
CURSOR_COLOR = (255, 50, 50)  # 赤
CURSOR_CENTER_DOT_SIZE = 4
CURSOR_CENTER_DOT_COLOR = (255, 255, 255)  # 白

# マウス設定
MOUSE_SENSITIVITY = 1.0

# ゲームパッド設定
GAMEPAD_SENSITIVITY = 500.0  # ピクセル/秒
GAMEPAD_DEADZONE = 0.15  # デッドゾーン (0.0 - 0.3)
GAMEPAD_RESPONSE_CURVE = 1.0  # 1.0 = Linear, 2.0+ = Exponential

# 反応曲線タイプ
class ResponseCurve:
    LINEAR = 1.0
    EXPONENTIAL = 2.0
    EXPONENTIAL_STRONG = 3.0

# 色定義
COLOR_BACKGROUND = (20, 20, 30)
COLOR_TEXT = (220, 220, 220)
COLOR_ACCENT = (100, 200, 255)
COLOR_SUCCESS = (100, 255, 150)
COLOR_WARNING = (255, 200, 100)

# デバイスタイプ
class DeviceType:
    MOUSE = "mouse"
    GAMEPAD = "gamepad"
