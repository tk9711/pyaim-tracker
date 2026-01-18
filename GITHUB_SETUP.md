# GitHubへのアップロード手順

このドキュメントでは、PyAim Cross-Platform TrackerをGitHubにアップロードする手順を説明します。

---

## 前提条件

- Gitがインストールされていること
- GitHubアカウントを持っていること

### Gitのインストール確認

```bash
git --version
```

インストールされていない場合：
- **Windows**: [Git for Windows](https://git-scm.com/download/win)
- **macOS**: `brew install git` または Xcode Command Line Tools
- **Linux**: `sudo apt install git`

---

## 手順

### 1. GitHubで新しいリポジトリを作成

1. [GitHub](https://github.com)にログイン
2. 右上の「+」→「New repository」をクリック
3. リポジトリ情報を入力：
   - **Repository name**: `pyaim-tracker` (または任意の名前)
   - **Description**: `Cross-platform aim training tool for FPS/TPS games`
   - **Public** または **Private** を選択
   - **Initialize this repository with:** すべてチェックを外す
4. 「Create repository」をクリック

### 2. ローカルリポジトリの初期化

ターミナルでプロジェクトディレクトリに移動：

```bash
cd /Users/tk/Downloads/TrackingAim
```

Gitリポジトリを初期化：

```bash
git init
git add .
git commit -m "Initial commit: PyAim Cross-Platform Tracker"
```

### 3. GitHubリポジトリに接続

GitHubで作成したリポジトリのURLを使用（例）：

```bash
git remote add origin https://github.com/YOUR_USERNAME/pyaim-tracker.git
git branch -M main
git push -u origin main
```

**注意**: `YOUR_USERNAME`を自分のGitHubユーザー名に置き換えてください。

### 4. 認証

初回プッシュ時に認証が求められます：

#### Personal Access Token（推奨）

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 「Generate new token」をクリック
3. スコープで「repo」を選択
4. トークンを生成してコピー
5. パスワードの代わりにトークンを使用

#### SSH（代替方法）

```bash
# SSH鍵を生成
ssh-keygen -t ed25519 -C "your_email@example.com"

# 公開鍵をコピー
cat ~/.ssh/id_ed25519.pub

# GitHubのSettings → SSH and GPG keys → New SSH keyに追加

# リモートURLをSSHに変更
git remote set-url origin git@github.com:YOUR_USERNAME/pyaim-tracker.git
```

---

## 更新のプッシュ

コードを変更した後：

```bash
git add .
git commit -m "説明的なコミットメッセージ"
git push
```

---

## ブランチ戦略（推奨）

開発用ブランチを作成：

```bash
# 開発ブランチを作成
git checkout -b develop

# 変更をコミット
git add .
git commit -m "Add new feature"

# GitHubにプッシュ
git push -u origin develop
```

---

## .gitignoreの確認

以下のファイル/フォルダは自動的に除外されます：

- `.venv/` - 仮想環境
- `__pycache__/` - Pythonキャッシュ
- `data/sessions/*.csv` - セッションデータ（オプション）
- `profiles/*.json` - プロファイル（オプション）
- `.vscode/` - VS Code設定

**セッションデータやプロファイルを含めたい場合**は、`.gitignore`から該当行を削除してください。

---

## README.mdの更新

GitHubで表示されるREADME.mdを充実させるために、以下を追加することを推奨：

- スクリーンショット
- デモGIF
- バッジ（ライセンス、Python version等）
- コントリビューションガイドライン

---

## トラブルシューティング

### エラー: "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/pyaim-tracker.git
```

### エラー: "failed to push some refs"

```bash
git pull origin main --rebase
git push
```

### 大きなファイルのエラー

Git LFSを使用：

```bash
git lfs install
git lfs track "*.png"
git add .gitattributes
git commit -m "Add Git LFS"
```

---

## 完了！

リポジトリURL: `https://github.com/YOUR_USERNAME/pyaim-tracker`

他の人が使えるように、README.mdに明確なインストール手順を記載しましょう。
