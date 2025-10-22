# Complete Claude Skill Integration

## Why

現在のエコマップ作成スキルは基本的な設計とモジュール実装が完了していますが、Claude Agent Skillとして動作するために必要な以下の要素が不足しています：

1. **対話型インターフェースの欠如** - ユーザーとの質問応答形式でデータを収集する機能がない
2. **SKILL.mdのYAML frontmatter不足** - Claude Skillとして認識されるために必要なメタデータがない
3. **uv対応の未実装** - モダンなPythonパッケージ管理ツールuvへの移行が必要
4. **統合スクリプトの未完成** - `ecomap_creator.py`の実装が完了していない

これらを実装することで、Claude Desktopから「田中一郎さんのエコマップを作成してください」と依頼すると、Claudeが対話的に情報を収集し、視覚的に優れたエコマップを自動生成できるようになります。

## What Changes

### 1. 対話型インターフェースの追加
- [ ] `modules/interactive_dialog.py` - 質問応答形式でのデータ収集エンジン
- [ ] 段階的な情報入力サポート（本人情報→家族→手帳→サービス...）
- [ ] 入力データの検証とフィードバック
- [ ] 既存Excelテンプレートとの互換性維持

### 2. SKILL.md改善
- [ ] YAML frontmatterの追加（name, description, version, dependencies）
- [ ] Claude Skillとしての使用方法の明確化
- [ ] 対話型モードとExcelモードの両方をサポート

### 3. uv統合
- [ ] `pyproject.toml`の作成（PEP 621準拠）
- [ ] `uv.lock`によるパッケージ管理
- [ ] uvコマンドでの実行サポート（`uv run ecomap-creator`）
- [ ] 既存のrequirements.txtとの互換性維持

### 4. メインスクリプト完成
- [ ] `ecomap_creator.py`の実装完了
- [ ] 既存モジュールの統合（excel_reader, node_generator, relation_generator等）
- [ ] エラーハンドリングとロギング
- [ ] 対話モードとファイルモードの切り替え

### 5. Claude Desktop統合
- [ ] ZIPパッケージング自動化スクリプト
- [ ] インストール手順書（README_INSTALLATION.md）
- [ ] テストケースとサンプルデータ検証

## Impact

### 影響を受ける機能領域
- **新規追加**: interactive-dialog（対話型データ収集）
- **新規追加**: uv-integration（モダンなパッケージ管理）
- **変更**: skill-metadata（SKILL.mdのフォーマット改善）
- **変更**: main-script（ecomap_creator.pyの完成）

### 影響を受けるファイル
- `SKILL.md` - YAML frontmatter追加
- `ecomap_creator.py` - 実装完了
- `modules/interactive_dialog.py` - 新規作成
- `pyproject.toml` - 新規作成
- `README.md` - インストール手順の更新
- `requirements.txt` - uv互換性のため維持

### ユーザー影響
- **既存ユーザー**: Excelファイルからの生成は引き続き利用可能（後方互換性維持）
- **新規ユーザー**: Claude Desktopから対話的に利用可能に
- **インストール方法**: uvを使用した簡潔なセットアップ

### 技術的影響
- Python 3.9以上が必要（uv要件）
- Claude Desktop Pro/Max/Team/Enterpriseアカウントが必要
- 既存のモジュール設計は維持（破壊的変更なし）

## Non-Goals（このプロポーザルで対応しないこと）

- データベース連携機能
- クラウド同期機能
- 複数ケースの一括管理
- Web API提供
- モバイルアプリ対応

## Success Criteria

1. Claude Desktopから「エコマップを作成して」と依頼できる
2. 対話形式で必要な情報を収集できる
3. Excelファイルからの生成も引き続き動作する
4. `uv run ecomap-creator`でスキルを実行できる
5. ZIPファイルをClaude Desktopにアップロードして使用できる
6. すべてのテストケースが通過する
