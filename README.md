# PyAim Cross-Platform Tracker

マウスとゲームパッドに対応した、クロスプラットフォームのエイムトレーニングツールです。

## 対応プラットフォーム

- ✅ **Windows** (Windows 10/11)
- ✅ **macOS** (10.15以降)
- ✅ **Linux** (Ubuntu等)

---

## 必要要件

- Python 3.9以上
- pip (Pythonパッケージマネージャー)

---

## インストール方法

### Windows

1. **Pythonのインストール**
   - [Python公式サイト](https://www.python.org/downloads/)からPython 3.9以上をダウンロード
   - インストール時に「Add Python to PATH」にチェック

2. **プロジェクトのセットアップ**
```cmd
cd TrackingAim
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. **起動**
```cmd
python main.py
```

### macOS

1. **Pythonのインストール** (Homebrewを使用)
```bash
brew install python@3.9
```

2. **プロジェクトのセットアップ**
```bash
cd TrackingAim
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

3. **起動**
```bash
python3 main.py
```

### Linux (Ubuntu/Debian)

1. **Pythonのインストール**
```bash
sudo apt update
sudo apt install python3.9 python3-pip python3-venv
```

2. **プロジェクトのセットアップ**
```bash
cd TrackingAim
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

3. **起動**
```bash
python3 main.py
```

---

## 機能

### トレーニングモード

#### 1. Tracking (追いエイム)
- 動くターゲットを追い続ける
- T0率（Time on Target）を計測
- 時間設定: 10〜60秒

#### 2. Flicking (瞬間エイム)
- ランダムに出現するターゲットを素早くクリック
- 反応速度を計測
- ターゲット数: 5〜30個

### 入力デバイス

- **マウス**: 自動検出
- **ゲームパッド**: 自動検出（接続時）
  - デッドゾーン調整
  - 反応曲線設定（Linear/Exponential）
  - 感度調整

### データ記録

- セッション結果を自動保存 (CSV形式)
- 統計ダッシュボードで過去の成績を確認
- スコア推移グラフ表示

---

## ディレクトリ構造

```
TrackingAim/
├── main.py              # エントリーポイント
├── requirements.txt     # 依存パッケージ
├── src/                 # ソースコード
│   ├── game.py         # メインゲームループ
│   ├── scenes/         # 各画面
│   ├── ui/             # UIコンポーネント
│   └── effects.py      # エフェクト
├── data/               # データ保存先
│   └── sessions/       # セッションログ
└── profiles/           # 設定ファイル
```

---

## トラブルシューティング

### Windows: フォントが正しく表示されない
- MS Gothic、Meiryo、Yu Gothicのいずれかがインストールされていることを確認

### macOS: 権限エラー
```bash
chmod +x main.py
```

### Linux: Pygameのインストールエラー
```bash
sudo apt install python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```

---

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

---

## 開発者向け

### VS Codeでのデバッグ

`.vscode/launch.json`が設定済みです。F5キーで起動できます。

### 依存パッケージ

- pygame-ce 2.5+
- numpy 2.0+
