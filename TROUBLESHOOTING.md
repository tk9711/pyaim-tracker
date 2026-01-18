# ユーザー向けトラブルシューティングガイド

PyAim Trackerを実行できない場合の解決方法をまとめました。

---

## macOS

### 問題1: 「開発元を確認できないため開けません」

**原因:** macOSのセキュリティ機能（Gatekeeper）

**解決方法A（推奨）:**
1. `PyAimTracker.app`を**右クリック**
2. 「開く」を選択
3. 「開く」ボタンをクリック

**解決方法B（ターミナル）:**
```bash
# ダウンロードしたフォルダで実行
xattr -cr PyAimTracker.app
```

その後、ダブルクリックで起動できます。

---

### 問題2: 「破損しているため開けません」

**原因:** ダウンロード時の属性情報

**解決方法:**
```bash
# ターミナルで実行
cd /path/to/download/folder
xattr -cr PyAimTracker.app
sudo spctl --master-disable  # 一時的にGatekeeperを無効化
open PyAimTracker.app
sudo spctl --master-enable   # 再度有効化
```

---

### 問題3: アプリが起動しない（無反応）

**原因:** 依存ライブラリの問題

**解決方法:**
1. アプリを右クリック → 「パッケージの内容を表示」
2. `Contents/MacOS/PyAimTracker`を右クリック → 「ターミナルで開く」
3. エラーメッセージを確認

**よくあるエラー:**
- `dyld: Library not loaded`: システムライブラリが不足
  → macOSを最新版にアップデート

---

### 問題4: 「Intel Macでは動作しない」

**原因:** Apple Silicon（M1/M2/M3）専用でビルドされている可能性

**解決方法:**
Intel Mac用に再ビルドが必要です。開発者に連絡してください。

---

## Windows

### 問題1: 「WindowsによってPCが保護されました」

**原因:** Windows Defenderのスマートスクリーン

**解決方法:**
1. 「詳細情報」をクリック
2. 「実行」ボタンをクリック

**注意:** これは正常な動作です。アプリに署名がないため表示されます。

---

### 問題2: ウイルス対策ソフトが削除する

**原因:** 未署名の実行ファイルを誤検知

**解決方法A（一時的）:**
1. ウイルス対策ソフトを一時的に無効化
2. アプリを実行
3. 除外リストに追加

**解決方法B（推奨）:**
1. ウイルス対策ソフトの設定を開く
2. 「除外」または「ホワイトリスト」に追加
3. `PyAimTracker.exe`のパスを指定

**主要なウイルス対策ソフト:**
- **Windows Defender**: 設定 → ウイルスと脅威の防止 → 除外の追加
- **Avast**: 設定 → 一般 → 除外
- **Norton**: 設定 → ウイルス対策 → 除外/低リスク

---

### 問題3: 「MSVCP140.dllが見つかりません」

**原因:** Visual C++ Redistributableが未インストール

**解決方法:**
1. [Microsoft公式サイト](https://aka.ms/vs/17/release/vc_redist.x64.exe)からダウンロード
2. インストール
3. PCを再起動
4. アプリを再実行

---

### 問題4: 起動が非常に遅い

**原因:** 初回起動時の展開処理

**解決方法:**
- 初回は30秒〜1分かかる場合があります
- 2回目以降は高速になります
- ウイルススキャンが原因の場合は除外リストに追加

---

### 問題5: 「アクセスが拒否されました」

**原因:** 管理者権限が必要

**解決方法:**
1. `PyAimTracker.exe`を右クリック
2. 「管理者として実行」を選択

---

## Linux

### 問題1: 「Permission denied」

**原因:** 実行権限がない

**解決方法:**
```bash
chmod +x PyAimTracker
./PyAimTracker
```

---

### 問題2: 「error while loading shared libraries」

**原因:** 必要なライブラリが不足

**解決方法（Ubuntu/Debian）:**
```bash
sudo apt update
sudo apt install -y \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libportaudio2
```

**解決方法（Fedora/RHEL）:**
```bash
sudo dnf install -y \
    SDL2 \
    SDL2_image \
    SDL2_mixer \
    SDL2_ttf \
    portaudio
```

---

### 問題3: 画面が真っ黒

**原因:** グラフィックドライバーの問題

**解決方法:**
```bash
# ソフトウェアレンダリングで起動
SDL_VIDEODRIVER=x11 ./PyAimTracker
```

---

## 共通の問題

### 問題1: 日本語が文字化けする

**macOS:**
- システムフォントが自動選択されるため、通常は問題なし

**Windows:**
- MS Gothic、Meiryo、Yu Gothicのいずれかがインストールされているか確認

**Linux:**
```bash
sudo apt install fonts-noto-cjk
```

---

### 問題2: ゲームパッドが認識されない

**解決方法:**
1. ゲームパッドを接続し直す
2. アプリを再起動
3. 別のUSBポートを試す
4. ゲームパッドのドライバーを更新

**対応コントローラー:**
- Xbox Controller
- PlayStation Controller
- 一般的なUSBゲームパッド

---

### 問題3: データが保存されない

**原因:** 書き込み権限がない

**解決方法:**
- アプリを「ドキュメント」フォルダに移動
- または管理者権限で実行

**データ保存場所:**
- macOS: `アプリと同じフォルダ/data/sessions/`
- Windows: `アプリと同じフォルダ\data\sessions\`

---

### 問題4: 画面サイズがおかしい

**原因:** 高DPI設定

**Windows解決方法:**
1. `PyAimTracker.exe`を右クリック
2. プロパティ → 互換性タブ
3. 「高DPI設定の変更」
4. 「高いDPIスケールの動作を上書きします」にチェック
5. 「アプリケーション」を選択

---

## それでも解決しない場合

### 1. ログファイルを確認

**macOS:**
```bash
# ターミナルで実行してエラーを確認
/Applications/PyAimTracker.app/Contents/MacOS/PyAimTracker
```

**Windows:**
```cmd
# コマンドプロンプトで実行
cd C:\path\to\app
PyAimTracker.exe
```

### 2. GitHubでIssueを作成

以下の情報を含めて報告してください：

```
【環境情報】
- OS: Windows 11 / macOS 14.0 / Ubuntu 22.04 など
- バージョン: v1.0.0
- ダウンロード元: GitHub Releases

【問題の詳細】
- 何をしたか
- どんなエラーが出たか
- エラーメッセージ（あれば）
- スクリーンショット（あれば）
```

報告先: https://github.com/tk9711/pyaim-tracker/issues

---

## 開発者向け: ソースからビルド

実行ファイルで問題がある場合、ソースコードから直接実行できます：

```bash
# リポジトリをクローン
git clone https://github.com/tk9711/pyaim-tracker.git
cd pyaim-tracker

# 仮想環境を作成
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 依存パッケージをインストール
pip install -r requirements.txt

# 実行
python3 main.py
```

---

## よくある質問

### Q: Pythonがインストールされていないと動きませんか？
**A:** いいえ。実行ファイル（.exe/.app）にはPythonが含まれているため、インストール不要です。

### Q: ファイルサイズが大きいのはなぜ？
**A:** Python本体と必要なライブラリがすべて含まれているためです。

### Q: ウイルスではありませんか？
**A:** 安全です。オープンソースで、コードはGitHubで公開されています。

### Q: 商用利用できますか？
**A:** はい。MITライセンスで自由に使用できます。

---

## サポート

- **GitHub Issues**: https://github.com/tk9711/pyaim-tracker/issues
- **マニュアル**: https://github.com/tk9711/pyaim-tracker/blob/main/MANUAL.md
- **ソースコード**: https://github.com/tk9711/pyaim-tracker
