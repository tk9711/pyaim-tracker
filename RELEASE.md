# GitHub Releasesでの配布手順

## 概要

他のユーザーがPythonをインストールせずにすぐに使えるよう、実行ファイルをGitHub Releasesで配布します。

---

## 手順

### 1. 実行ファイルをビルド

#### macOS（現在の環境）
```bash
cd /Users/tk/Downloads/TrackingAim
source .venv/bin/activate
pip install pyinstaller
./build.sh
```

ビルド後、`dist/PyAimTracker.app`が作成されます。

#### Windows（別のPCが必要）
```cmd
cd TrackingAim
.venv\Scripts\activate
pip install pyinstaller
build.bat
```

ビルド後、`dist/PyAimTracker.exe`が作成されます。

---

### 2. ZIPファイルを作成

#### macOS
```bash
cd dist
zip -r PyAimTracker-macOS-v1.0.0.zip PyAimTracker.app
```

#### Windows
```cmd
# distフォルダを右クリック → 送る → 圧縮フォルダー
# ファイル名: PyAimTracker-Windows-v1.0.0.zip
```

---

### 3. GitHub Releasesにアップロード

1. **GitHubリポジトリにアクセス**
   https://github.com/tk9711/pyaim-tracker

2. **Releasesページに移動**
   - 「Releases」タブをクリック
   - 「Create a new release」をクリック

3. **リリース情報を入力**
   - **Tag**: `v1.0.0`
   - **Release title**: `PyAim Tracker v1.0.0`
   - **Description**:
   ```markdown
   # PyAim Cross-Platform Tracker v1.0.0
   
   マウスとゲームパッドに対応したエイムトレーニングツールの初回リリースです。
   
   ## 主な機能
   - **Trackingモード**: 動くターゲットを追従（T0率計測）
   - **Flickingモード**: 瞬間エイム（反応速度計測）
   - **統計機能**: セッション履歴とグラフ表示
   - **カスタマイズ**: 時間、ターゲット数、感度調整
   
   ## ダウンロード
   
   お使いのOSに合わせてダウンロードしてください：
   
   - **macOS**: PyAimTracker-macOS-v1.0.0.zip
   - **Windows**: PyAimTracker-Windows-v1.0.0.zip
   
   ## インストール方法
   
   ### macOS
   1. ZIPファイルを解凍
   2. `PyAimTracker.app`をダブルクリック
   3. 「開発元を確認できません」と表示された場合:
      - 右クリック → 「開く」
      - または: `xattr -cr PyAimTracker.app` を実行
   
   ### Windows
   1. ZIPファイルを解凍
   2. `PyAimTracker.exe`をダブルクリック
   3. 「WindowsによってPCが保護されました」と表示された場合:
      - 「詳細情報」→「実行」をクリック
   
   ## システム要件
   - **OS**: Windows 10/11、macOS 10.15以降
   - **メモリ**: 2GB以上推奨
   - **ディスプレイ**: 1280x720以上
   
   ## 問題が発生した場合
   - [Issues](https://github.com/tk9711/pyaim-tracker/issues)で報告してください
   - [マニュアル](https://github.com/tk9711/pyaim-tracker/blob/main/MANUAL.md)を参照
   ```

4. **ファイルをアップロード**
   - 「Attach binaries」エリアにZIPファイルをドラッグ&ドロップ
   - または「choose your files」をクリックして選択

5. **公開**
   - 「Publish release」をクリック

---

### 4. ユーザーの使い方

ユーザーは以下の手順で使用できます：

1. https://github.com/tk9711/pyaim-tracker/releases にアクセス
2. 最新版のZIPファイルをダウンロード
3. 解凍して実行ファイルをダブルクリック
4. すぐにトレーニング開始！

**Pythonのインストール不要**で使えます。

---

## 注意事項

### macOS
- 初回起動時にセキュリティ警告が出る場合があります
- 右クリック→「開く」で起動してください

### Windows
- Windows Defenderの警告が出る場合があります
- 「詳細情報」→「実行」で起動してください

### ファイルサイズ
- macOS: 約60-80MB
- Windows: 約50-70MB

---

## 更新時の手順

新しいバージョンをリリースする場合：

1. コードを更新
2. 実行ファイルを再ビルド
3. 新しいタグ（例: `v1.1.0`）でリリース作成
4. 変更内容をリリースノートに記載

---

## まとめ

この方法により：
- ✅ Pythonがインストールされていない環境でも動作
- ✅ ダウンロードしてすぐに使える
- ✅ Gitリポジトリサイズに影響しない
- ✅ バージョン管理が明確

ユーザーフレンドリーな配布が実現できます！
