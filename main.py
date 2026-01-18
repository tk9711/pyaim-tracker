#!/usr/bin/env python3
"""
PyAim Cross-Platform Tracker
マウスとゲームパッドの両方に対応したエイムトレーニングツール
"""

from src.game import Game


def main():
    """エントリーポイント"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
