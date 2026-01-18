"""
プロファイル保存/読み込みモジュール
"""

import json
import os
from typing import Dict, Any, Optional
from .settings import (
    MOUSE_SENSITIVITY,
    GAMEPAD_SENSITIVITY,
    GAMEPAD_DEADZONE,
    GAMEPAD_RESPONSE_CURVE,
)


PROFILE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "profiles")
DEFAULT_PROFILE_PATH = os.path.join(PROFILE_DIR, "default.json")


def get_default_profile() -> Dict[str, Any]:
    """デフォルトプロファイルを取得"""
    return {
        "mouse": {
            "sensitivity": MOUSE_SENSITIVITY,
        },
        "gamepad": {
            "sensitivity": GAMEPAD_SENSITIVITY,
            "deadzone": GAMEPAD_DEADZONE,
            "response_curve": GAMEPAD_RESPONSE_CURVE,
        }
    }


def save_profile(profile: Dict[str, Any], path: Optional[str] = None) -> bool:
    """
    プロファイルを保存
    
    Args:
        profile: プロファイルデータ
        path: 保存先パス（Noneの場合はデフォルトパス）
        
    Returns:
        True: 成功, False: 失敗
    """
    if path is None:
        path = DEFAULT_PROFILE_PATH
    
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"プロファイル保存エラー: {e}")
        return False


def load_profile(path: Optional[str] = None) -> Dict[str, Any]:
    """
    プロファイルを読み込み
    
    Args:
        path: 読み込み元パス（Noneの場合はデフォルトパス）
        
    Returns:
        プロファイルデータ（存在しない場合はデフォルト）
    """
    if path is None:
        path = DEFAULT_PROFILE_PATH
    
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"プロファイル読み込みエラー: {e}")
    
    return get_default_profile()


def apply_profile_to_input_handler(profile: Dict[str, Any], input_handler) -> None:
    """プロファイルをInputHandlerに適用"""
    mouse = profile.get("mouse", {})
    gamepad = profile.get("gamepad", {})
    
    input_handler.set_mouse_sensitivity(mouse.get("sensitivity", MOUSE_SENSITIVITY))
    input_handler.set_gamepad_sensitivity(gamepad.get("sensitivity", GAMEPAD_SENSITIVITY))
    input_handler.set_deadzone(gamepad.get("deadzone", GAMEPAD_DEADZONE))
    input_handler.set_response_curve(gamepad.get("response_curve", GAMEPAD_RESPONSE_CURVE))


def create_profile_from_input_handler(input_handler) -> Dict[str, Any]:
    """InputHandlerから現在の設定をプロファイルとして作成"""
    return {
        "mouse": {
            "sensitivity": input_handler.mouse_sensitivity,
        },
        "gamepad": {
            "sensitivity": input_handler.gamepad_sensitivity,
            "deadzone": input_handler.deadzone,
            "response_curve": input_handler.response_curve,
        }
    }
