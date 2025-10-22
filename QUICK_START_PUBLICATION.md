# 🚀 公開クイックスタートガイド

## ✅ 既に完了した準備

- [x] LICENSE ファイル追加（MIT License）
- [x] .gitignore 設定
- [x] CHANGELOG.md 作成
- [x] CONTRIBUTING.md 作成
- [x] pyproject.toml ライセンス更新
- [x] README.md ライセンス情報追加

## 📝 次に実行すべき3つのステップ

### ステップ1: 個人情報の更新（5分）

**pyproject.toml の更新**:
```toml
authors = [
    { name = "K. Kawahara", email = "your-actual-email@example.com" }
]

[project.urls]
Homepage = "https://github.com/kazumasakawahara/ecomap-creator"
Documentation = "https://github.com/kazumasakawahara/ecomap-creator/blob/main/SKILL.md"
Repository = "https://github.com/kazumasakawahara/ecomap-creator"
Issues = "https://github.com/kazumasakawahara/ecomap-creator/issues"
```

**CONTRIBUTING.md の更新**:
- Email欄を実際のメールアドレスに変更

### ステップ2: GitHubリポジトリ作成（10分）

1. **GitHubで新規リポジトリ作成**
   - リポジトリ名: `ecomap-creator`
   - 説明: "知的障害・精神障害のある方の支援情報を一元管理し、視覚的なエコマップとして表示するClaude Agent Skill"
   - Public/Private選択
   - **「Add README」「Add .gitignore」「Add license」はチェックしない**（既にあるため）

2. **ローカルでGit初期化とプッシュ**
   ```bash
   # プロジェクトディレクトリで実行
   cd /Users/k-kawahara/Ai-Workspace/ecomap-creator

   # Git初期化
   git init

   # ステージング
   git add .

   # 初回コミット
   git commit -m "feat: initial release v1.1.0

- Complete interactive dialog engine
- Excel template with 10 sheets
- Support for disability support data management
- Test coverage: 9/10 tests passing"

   # ブランチ名をmainに変更
   git branch -M main

   # リモート追加（kazumasakawaharaを実際のものに変更）
   git remote add origin https://github.com/kazumasakawahara/ecomap-creator.git

   # プッシュ
   git push -u origin main
   ```

3. **GitHubリポジトリ設定**
   - About → Topics追加: `ecomap`, `disability-support`, `claude-skill`, `social-work`, `python`
   - Settings → Features → Issues有効化
   - Settings → Features → Discussions有効化（任意）

### ステップ3: リリース作成（10分）

1. **タグ作成**
   ```bash
   git tag -a v1.1.0 -m "Release v1.1.0

New Features:
- Excel template with 10 sheets
- Complete interactive dialog implementation
- Basic test suite

Improvements:
- Detailed data collection for all categories
- Flexible input handling
- Japanese era date support"

   git push origin v1.1.0
   ```

2. **GitHub Releaseページでリリース作成**
   - Releases → Create a new release
   - タグ: `v1.1.0`
   - タイトル: `v1.1.0 - Interactive Mode Complete`
   - 説明: 下記をコピー

```markdown
## 🎉 Version 1.1.0 - Interactive Mode Complete

### ✨ New Features
- 📝 **Excel Template**: 10-sheet template with sample data
- 💬 **Complete Interactive Dialog**: All categories now collect detailed data
- 🧪 **Test Suite**: 9/10 tests passing (90% coverage)

### 🔧 Improvements
- Flexible input handling (skip, next, multiple expressions)
- Japanese era date support (令和/平成/昭和)
- Multiple item registration (notebooks, diagnoses, services)

### 📦 Installation

#### For Claude Desktop Users
1. Download `ecomap-creator-v1.1.0.zip` from Assets below
2. Open Claude Desktop
3. Settings → Skills → Upload Skill
4. Select the downloaded ZIP file

#### For Developers
```bash
git clone https://github.com/kazumasakawahara/ecomap-creator.git
cd ecomap-creator
uv sync
```

### 🚀 Usage

**Interactive Mode (Recommended)**:
```
「田中一郎さんのエコマップを作成してください」
```

**File Mode**:
```bash
uv run ecomap-creator samples/sample_case_01.xlsx
```

### 📚 Documentation
- [SKILL.md](https://github.com/kazumasakawahara/ecomap-creator/blob/main/SKILL.md) - Claude Skill usage guide
- [README.md](https://github.com/kazumasakawahara/ecomap-creator/blob/main/README.md) - Detailed documentation
- [CHANGELOG.md](https://github.com/kazumasakawahara/ecomap-creator/blob/main/CHANGELOG.md) - Version history

### 🐛 Known Issues
- One test failing in date converter (invalid date handling)

### 🤝 Contributing
See [CONTRIBUTING.md](https://github.com/kazumasakawahara/ecomap-creator/blob/main/CONTRIBUTING.md)

### 📄 License
MIT License - see [LICENSE](https://github.com/kazumasakawahara/ecomap-creator/blob/main/LICENSE)
```

3. **Assets添付**
   - `ecomap-creator-v1.1.0.zip` をアップロード（DesktopにあるZIPファイル）

4. **Publish release** クリック

## 🎊 完了！

これで公開完了です。以下を確認してください：

- [ ] GitHubリポジトリが公開されている
- [ ] v1.1.0 リリースが表示されている
- [ ] ZIPファイルがダウンロード可能
- [ ] README.mdが適切に表示されている

## 📢 次のステップ（任意）

### コミュニティに共有
- Twitter/X で公開告知
- Qiita/Zennで技術記事執筆
- Claude公式フォーラム（あれば）で紹介

### 継続的改善
- GitHub Issuesでフィードバック収集
- 月1回の依存関係更新
- バグ修正とマイナーアップデート

---

**所要時間**: 合計約25分
**難易度**: 初級〜中級

何か問題があれば、PUBLICATION_CHECKLIST.mdの詳細版を参照してください。
