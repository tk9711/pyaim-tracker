@echo off
REM Windows用ビルドスクリプト

echo PyAim Tracker - ビルドスクリプト
echo ================================

REM 仮想環境の確認
if not exist ".venv" (
    echo エラー: 仮想環境が見つかりません
    echo python -m venv .venv を実行してください
    exit /b 1
)

REM 仮想環境をアクティベート
call .venv\Scripts\activate.bat

REM PyInstallerのインストール確認
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstallerをインストール中...
    pip install pyinstaller
)

REM 古いビルドを削除
echo 古いビルドをクリーンアップ中...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM ビルド実行
echo ビルド中...
pyinstaller PyAimTracker.spec

REM 結果確認
if %errorlevel% equ 0 (
    echo.
    echo ✅ ビルド成功！
    echo.
    echo 実行ファイルの場所:
    echo   dist\PyAimTracker.exe
    echo.
    echo 起動方法:
    echo   dist\PyAimTracker.exe をダブルクリック
    echo.
    echo 配布方法:
    echo   distフォルダをZIPで圧縮して配布してください
) else (
    echo.
    echo ❌ ビルド失敗
    echo エラーログを確認してください
    exit /b 1
)

pause
