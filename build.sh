#!/bin/bash
# macOS/Linux用ビルドスクリプト

echo "PyAim Tracker - ビルドスクリプト"
echo "================================"

# 仮想環境の確認
if [ ! -d ".venv" ]; then
    echo "エラー: 仮想環境が見つかりません"
    echo "python3 -m venv .venv を実行してください"
    exit 1
fi

# 仮想環境をアクティベート
source .venv/bin/activate

# PyInstallerのインストール確認
if ! pip show pyinstaller > /dev/null 2>&1; then
    echo "PyInstallerをインストール中..."
    pip install pyinstaller
fi

# 古いビルドを削除
echo "古いビルドをクリーンアップ中..."
rm -rf build dist

# ビルド実行
echo "ビルド中..."
pyinstaller PyAimTracker.spec

# 結果確認
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ビルド成功！"
    echo ""
    echo "実行ファイルの場所:"
    
    if [ "$(uname)" == "Darwin" ]; then
        # macOS
        echo "  dist/PyAimTracker.app"
        echo ""
        echo "起動方法:"
        echo "  open dist/PyAimTracker.app"
    else
        # Linux
        echo "  dist/PyAimTracker"
        echo ""
        echo "起動方法:"
        echo "  ./dist/PyAimTracker"
    fi
    
    echo ""
    echo "配布方法:"
    echo "  distフォルダをZIPで圧縮して配布してください"
else
    echo ""
    echo "❌ ビルド失敗"
    echo "エラーログを確認してください"
    exit 1
fi
