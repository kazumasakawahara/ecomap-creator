# Ecomap Creator Skill 公開チェックリスト

## Phase 1: 準備（1-2日）

### 1.1 ライセンス決定と追加
- [ ] ライセンスを選定（推奨: MIT License）
- [ ] LICENSEファイル作成
- [ ] pyproject.tomlのlicense更新
- [ ] README.mdにライセンス情報追加

### 1.2 個人情報の確認
- [ ] サンプルデータに実在する個人名がないか確認
- [ ] 作者情報の確認（email addressを実際のものに）
- [ ] 機密情報（APIキー、パスワード等）が含まれていないか確認

### 1.3 ドキュメント整備
- [ ] README.mdの最終確認
  - [ ] インストール手順が明確か
  - [ ] 使用例が十分か
  - [ ] トラブルシューティングが充実しているか
- [ ] SKILL.mdの最終確認
- [ ] CHANGELOG.md作成（バージョン履歴）
- [ ] CONTRIBUTING.md作成（任意、貢献ガイド）

### 1.4 コード品質チェック
- [ ] すべてのテストが通過するか確認
- [ ] コードフォーマット（black/ruff）実行
- [ ] 不要なコメント、デバッグコードの削除
- [ ] TODOコメントの確認・対応

---

## Phase 2: GitHubリポジトリ作成（1日）

### 2.1 リポジトリ作成
- [ ] GitHubアカウント確認
- [ ] 新規リポジトリ作成
  - リポジトリ名: `ecomap-creator`
  - 説明: "知的障害・精神障害のある方の支援情報を一元管理し、視覚的なエコマップとして表示するClaude Agent Skill"
  - Public/Private選択
  - README、LICENSE、.gitignore追加

### 2.2 .gitignore設定
```
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.venv/
*.egg-info/
dist/
build/
.DS_Store
outputs/
*.zip
.claude/
```

### 2.3 初回コミット
```bash
git init
git add .
git commit -m "feat: initial release v1.1.0

- Interactive dialog engine for ecomap creation
- Excel template with 10 sheets
- Support for disability support data management
- Test coverage: 9/10 tests passing"
git branch -M main
git remote add origin https://github.com/[username]/ecomap-creator.git
git push -u origin main
```

### 2.4 リポジトリ設定
- [ ] About設定（Topics追加: ecomap, disability-support, claude-skill）
- [ ] Issuesテンプレート作成（任意）
- [ ] GitHub Actionsでテスト自動化（任意）

---

## Phase 3: リリース作成（1日）

### 3.1 タグ作成
```bash
git tag -a v1.1.0 -m "Release v1.1.0

New Features:
- Excel template with 10 sheets
- Complete interactive dialog implementation
- Basic test suite

Improvements:
- Detailed data collection for all categories
- Flexible input handling (skip, next, etc.)
- Japanese era date support"

git push origin v1.1.0
```

### 3.2 GitHub Release作成
- [ ] GitHubのReleasesページで新規リリース作成
- [ ] タグ: v1.1.0
- [ ] リリースタイトル: "v1.1.0 - Interactive Mode Complete"
- [ ] リリースノート記載
- [ ] `ecomap-creator-v1.1.0.zip` をアセットとして添付

### 3.3 リリースノート内容
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
Download `ecomap-creator-v1.1.0.zip` and upload to Claude Desktop:
1. Settings → Skills → Upload Skill
2. Select the downloaded ZIP file

### 🚀 Usage
Claude Desktop:
「田中一郎さんのエコマップを作成してください」

### 📚 Documentation
- [SKILL.md](SKILL.md) - Claude Skill usage guide
- [README.md](README.md) - Detailed documentation
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Usage examples

### 🐛 Known Issues
- One test failing in date converter (invalid date handling)
```

---

## Phase 4: コミュニティ公開（継続）

### 4.1 Claude Community（もし存在すれば）
- [ ] Claude公式フォーラム/コミュニティで紹介
- [ ] 使用例とスクリーンショット共有

### 4.2 SNS/ブログ（任意）
- [ ] Twitter/X で公開告知
- [ ] Qiita/Zennで技術記事執筆
- [ ] 個人ブログで紹介記事

### 4.3 PyPI公開（任意、将来的に）
```bash
uv build
uv publish
```

---

## Phase 5: メンテナンス（継続）

### 5.1 Issue対応
- [ ] バグレポートへの対応
- [ ] 機能リクエストの評価
- [ ] ドキュメント改善要望への対応

### 5.2 バージョン管理
- [ ] セマンティックバージョニング遵守
  - v1.x.y: マイナー機能追加、バグフィックス
  - v2.0.0: 破壊的変更
- [ ] CHANGELOG.md更新

### 5.3 定期メンテナンス
- [ ] 依存関係の更新（月1回）
- [ ] セキュリティアップデート即時対応
- [ ] Python新バージョン対応

---

## 推奨公開タイムライン

```
Day 1-2:  Phase 1 (準備)
Day 3:    Phase 2 (GitHubリポジトリ)
Day 4:    Phase 3 (リリース)
Day 5-:   Phase 4-5 (コミュニティ、メンテナンス)
```

---

## 緊急度別チェック

### 🔴 必須（公開前に絶対必要）
- [ ] ライセンスファイル追加
- [ ] 個人情報・機密情報除去
- [ ] GitHubリポジトリ作成
- [ ] 実際のGitHub URLに更新

### 🟡 重要（公開時にあるべき）
- [ ] CHANGELOG.md作成
- [ ] .gitignore設定
- [ ] リリースノート作成
- [ ] テスト全通過

### 🟢 推奨（できれば）
- [ ] CONTRIBUTING.md作成
- [ ] GitHub Actions CI/CD
- [ ] コードフォーマット統一
- [ ] PyPI公開

---

## 連絡先・サポート

公開後のサポート方法を明記：
- GitHub Issues: バグ報告、機能リクエスト
- Email: 問い合わせ先（任意）
- Discussions: 使用方法の質問（GitHub Discussions有効化）
