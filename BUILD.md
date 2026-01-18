# 実行ファイルのビルド方法

このドキュメントでは、PyAim TrackerをPythonがインストールされていない環境でも動作するスタンドアロン実行ファイルにビルドする方法を説明します。

---

## 前提条件

- Python 3.9以上がインストールされていること
- 仮想環境（.venv）が作成されていること
- 必要なパッケージがインストールされていること

---

## ビルド手順

### macOS / Linux

```bash
# 実行権限を付与
chmod +x build.sh

# ビルド実行
./build.sh
```

### Windows

```cmd
# ビルド実行
build.bat
```

---

## ビルド結果

ビルドが成功すると、`dist`フォルダに実行ファイルが作成されます：

### macOS
```
dist/
└── PyAimTracker.app/
```

### Windows
```
dist/
└── PyAimTracker.exe
```

### Linux
```
dist/
└── PyAimTracker
```

---

## 配布方法

### 1. ZIPファイルで配布（推奨）

```bash
# macOS/Linux
cd dist
zip -r PyAimTracker-macOS.zip PyAimTracker.app

# Windows
# distフォルダを右クリック → 送る → 圧縮（zip形式）フォルダー
```

### 2. GitHubリリースで配布

1. GitHubリポジトリの「Releases」タブに移動
2. 「Create a new release」をクリック
3. タグ: `v1.0.0`
4. タイトル: `PyAim Tracker v1.0.0`
5. ZIPファイルをアップロード
6. 「Publish release」をクリック

---

## ファイルサイズ

- **macOS**: 約60-80MB
- **Windows**: 約50-70MB
- **Linux**: 約50-70MB

---

## トラブルシューティング

### エラー: "ModuleNotFoundError"

```bash
# 仮想環境で依存パッケージを再インストール
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
pip install pyinstaller
```

### エラー: "Permission denied"

```bash
# macOS/Linux
chmod +x build.sh
chmod +x dist/PyAimTracker  # Linux
```

### macOS: "開発元を確認できないため開けません"

```bash
# セキュリティ設定を一時的に解除
xattr -cr dist/PyAimTracker.app
```

または、システム環境設定 → セキュリティとプライバシー → 「このまま開く」

### Windows: "WindowsによってPCが保護されました"

「詳細情報」→「実行」をクリック

---

## 高度な設定

### アイコンの追加

1. アイコンファイル（.ico / .icns）を用意
2. `PyAimTracker.spec`を編集:

```python
exe = EXE(
    ...
    icon='path/to/icon.ico',  # Windowsの場合
    ...
)

app = BUNDLE(
    ...
    icon='path/to/icon.icns',  # macOSの場合
    ...
)
```

### ファイルサイズの削減

```bash
# UPX圧縮を有効化（既に有効）
# PyAimTracker.specで upx=True に設定済み
```

### デバッグモード

```python
# PyAimTracker.specを編集
exe = EXE(
    ...
    console=True,  # コンソールを表示
    debug=True,    # デバッグモード
    ...
)
```

---

## 配布時の注意事項

### README.txtを同梱

```
PyAim Tracker v1.0.0

【使い方】
1. PyAimTracker.exe（または.app）をダブルクリック
2. ランチャー画面でモードを選択
3. トレーニング開始！

【システム要件】
- Windows 10/11、macOS 10.15以降、またはLinux
- メモリ: 2GB以上推奨
- ディスプレイ: 1280x720以上

【問題が発生した場合】
GitHub: https://github.com/tk9711/pyaim-tracker
```

### ライセンス情報

`LICENSE`ファイルを同梱してください。

---

## 自動ビルド（GitHub Actions）

将来的にGitHub Actionsで自動ビルドを設定することも可能です。

---

## まとめ

1. `build.sh`（または`build.bat`）を実行
2. `dist`フォルダの内容をZIPで圧縮
3. GitHubリリースまたは他の方法で配布

これで、Pythonがインストールされていない環境でもアプリを実行できます！
