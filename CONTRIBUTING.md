# Contributing to Ecomap Creator

このプロジェクトへの貢献に興味を持っていただきありがとうございます！

## 貢献方法

### バグレポート

バグを見つけた場合は、以下の情報を含めてIssueを作成してください：

1. **環境情報**
   - OS（macOS, Windows, Linux）
   - Pythonバージョン
   - ecomap-creatorバージョン

2. **再現手順**
   - 何をしたか
   - 何が起きたか
   - 何が起きるべきだったか

3. **エラーメッセージ**（もしあれば）

### 機能リクエスト

新機能の提案は歓迎します！以下を含めてIssueを作成してください：

1. **ユースケース**: どのような場面で使いたいか
2. **期待される動作**: どのように動作すべきか
3. **代替案**: 他に考えられる方法はあるか

### プルリクエスト

1. **Fork & Clone**
   ```bash
   git clone https://github.com/[your-username]/ecomap-creator.git
   cd ecomap-creator
   ```

2. **環境セットアップ**
   ```bash
   uv sync --extra dev
   ```

3. **ブランチ作成**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **開発**
   - コードを書く
   - テストを追加
   - ドキュメントを更新

5. **テスト実行**
   ```bash
   uv run pytest tests/ -v
   ```

6. **コミット**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

7. **Push & Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## コーディング規約

### Pythonスタイル

- **PEP 8**に準拠
- **Black**でフォーマット（`uv run black .`）
- **Ruff**でLint（`uv run ruff check .`）

### コミットメッセージ

Conventional Commits形式を使用：

- `feat:` 新機能
- `fix:` バグ修正
- `docs:` ドキュメントのみの変更
- `test:` テストの追加・修正
- `refactor:` リファクタリング
- `chore:` ビルドプロセスやツールの変更

例:
```
feat: add support for CSV export
fix: resolve date parsing issue with Japanese era
docs: update installation guide for Windows
```

### テスト

- 新機能には必ずテストを追加
- 既存のテストが全て通過することを確認
- カバレッジを下げない

## プロジェクト構造

```
ecomap-creator/
├── ecomap_creator.py       # メインスクリプト
├── modules/                # コアモジュール
│   ├── excel_reader.py
│   ├── interactive_dialog.py
│   └── ...
├── tests/                  # テスト
├── templates/              # テンプレート
├── samples/                # サンプルデータ
└── docs/                   # ドキュメント
```

## 質問・サポート

- **GitHub Discussions**: 使用方法の質問
- **GitHub Issues**: バグ報告、機能リクエスト
- **Email**: [your-email]（緊急時のみ）

## 行動規範

このプロジェクトは、誰もが安心して貢献できる環境を目指しています：

- 敬意を持って接する
- 建設的なフィードバックを心がける
- 多様性を尊重する
- プライバシーを守る

不適切な行動を見かけた場合は、プロジェクトメンテナーに報告してください。

## ライセンス

貢献したコードはMITライセンスの下で公開されます。

---

貢献をお待ちしています！🎉
