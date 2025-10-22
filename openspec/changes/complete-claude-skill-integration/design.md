# Design Document: Complete Claude Skill Integration

## Context

エコマップ作成スキルは、知的・精神障害者向けの支援情報を視覚化するツールです。現在、基本的なモジュール設計は完了していますが、Claude Agent Skillとして動作するためには対話型インターフェース、uv統合、メインスクリプトの実装が必要です。

### 背景
- **ユーザー**: 相談支援専門員（計画相談支援の担当者）
- **利用場面**: ケース会議、サービス等利用計画作成、引き継ぎ資料、モニタリング
- **対象地域**: 北九州市および隣接市町村

### 制約
- Python 3.9以上（uv要件）
- Claude Desktop Pro/Max/Team/Enterpriseアカウント
- ローカル環境で動作（外部サーバー通信なし）
- 個人情報保護の観点からセキュアな実装が必要

## Goals / Non-Goals

### Goals
1. Claude Desktopから対話的にエコマップを作成できる
2. Excelファイルからの生成も引き続き利用可能（後方互換性）
3. uvを使用した簡潔なセットアップ
4. エラーハンドリングとユーザーフィードバックの充実

### Non-Goals
- データベース連携（将来的な拡張）
- Web API提供
- クラウド同期機能
- 複数ユーザー管理

## Decisions

### 1. 対話型エンジンの設計

**決定**: ステートマシンパターンを使用した段階的データ収集

**理由**:
- 情報の種類が多岐にわたる（本人、家族、手帳、支援区分、診断、サービス等）
- ユーザーが途中で入力を中断・再開する可能性がある
- 各段階で入力の検証とフィードバックが必要

**実装アプローチ**:
```python
class InteractiveDialogEngine:
    def __init__(self):
        self.state = "INITIAL"
        self.collected_data = {}

    def start_session(self):
        self.state = "COLLECT_PERSON"
        return self.get_questions_for_state()

    def process_input(self, user_input):
        if self.state == "COLLECT_PERSON":
            self.collected_data["person"] = self.parse_person_info(user_input)
            self.state = "COLLECT_FAMILY"
        # ... 他の状態遷移
```

**状態遷移**:
```
INITIAL → COLLECT_PERSON → COLLECT_FAMILY → COLLECT_NOTEBOOK
→ COLLECT_SUPPORT_LEVEL → COLLECT_SERVICE → COLLECT_MEDICAL → COMPLETE
```

**代替案として検討したもの**:
- **一括入力フォーム**: 却下（情報量が多すぎて対話に適さない）
- **自由形式対話**: 却下（構造化データの抽出が困難）

### 2. uv統合戦略

**決定**: pyproject.tomlを使用したPEP 621準拠の設定

**理由**:
- uvはpyproject.tomlをネイティブサポート
- requirements.txtより高機能（メタデータ、スクリプトエントリポイント等）
- Pythonパッケージングの標準規格

**pyproject.toml構造**:
```toml
[project]
name = "ecomap-creator"
version = "1.0.0"
description = "知的・精神障害者向けエコマップ作成スキル"
requires-python = ">=3.9"
dependencies = [
    "openpyxl>=3.1.5",
]

[project.scripts]
ecomap-creator = "ecomap_creator:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**代替案として検討したもの**:
- **requirements.txt継続**: 却下（uvの利点を活かせない）
- **setup.py使用**: 却下（レガシーなアプローチ）

### 3. モード判定ロジック

**決定**: コマンドライン引数の有無で自動判定

**理由**:
- ユーザーの意図が明確
- シンプルで理解しやすい

**実装**:
```python
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", nargs="?", help="Excel file path")
    parser.add_argument("--interactive", "-i", action="store_true")
    args = parser.parse_args()

    if args.input_file:
        # ファイルモード
        creator = EcomapCreator(input_file=args.input_file)
    elif args.interactive or sys.stdin.isatty():
        # 対話モード
        creator = EcomapCreator(interactive=True)
    else:
        parser.print_help()
```

**代替案として検討したもの**:
- **環境変数による切り替え**: 却下（ユーザーに不便）
- **設定ファイルによる指定**: 却下（過度に複雑）

### 4. データ検証戦略

**決定**: 既存のValidatorクラスを拡張し、対話モードとファイルモードで共通化

**理由**:
- コードの重複を避ける
- 一貫した検証ロジック
- 保守性の向上

**実装アプローチ**:
```python
# modules/validator.py (既存)
class Validator:
    @staticmethod
    def validate_person_info(data):
        errors = []
        if not data.get("name"):
            errors.append("氏名は必須です")
        if not data.get("birth_date"):
            errors.append("生年月日は必須です")
        return errors

# modules/interactive_dialog.py (新規)
from modules.validator import Validator

class InteractiveDialogEngine:
    def collect_person_info(self):
        # ... 質問と回答収集
        errors = Validator.validate_person_info(person_data)
        if errors:
            return self.provide_feedback(errors)
        # ... 次の状態へ
```

### 5. ZIPパッケージング

**決定**: シェルスクリプトによる自動化

**理由**:
- 手動作業のエラー削減
- バージョン管理の自動化
- 一貫性の確保

**package.shの構造**:
```bash
#!/bin/bash
VERSION=$(grep "version" pyproject.toml | cut -d'"' -f2)
OUTPUT="ecomap-creator-v${VERSION}.zip"

zip -r $OUTPUT \
    SKILL.md \
    ecomap_creator.py \
    modules/ \
    templates/ \
    samples/ \
    schema.json \
    pyproject.toml \
    README.md \
    -x "*.pyc" -x "__pycache__/*"
```

## Risks / Trade-offs

### Risk 1: 対話型モードの複雑性
**リスク**: 質問応答形式が複雑化し、ユーザー体験が悪化する可能性

**軽減策**:
- 段階的な情報収集（一度に聞く情報を限定）
- 明確な進捗表示（「5/10ステップ完了」等）
- スキップ可能なオプション項目
- 入力例の提示

### Risk 2: uv依存による導入障壁
**リスク**: uvのインストールが必要になることで、導入のハードルが上がる

**軽減策**:
- 詳細なインストール手順書の提供
- requirements.txtの維持（フォールバック）
- トラブルシューティングガイド

### Risk 3: 後方互換性の維持
**リスク**: 新機能追加により、既存のExcelテンプレートが動作しなくなる可能性

**軽減策**:
- 既存のExcelReaderモジュールは変更しない
- 新機能は追加のみ（破壊的変更なし）
- 既存サンプルデータでの回帰テスト

### Trade-off 1: 機能性 vs 複雑性
**選択**: シンプルさを優先し、高度な機能は将来的な拡張に残す

**理由**: 初期バージョンはMVP（Minimum Viable Product）として、基本機能の確実な動作を優先

### Trade-off 2: パフォーマンス vs 可読性
**選択**: 可読性を優先し、最適化は必要になってから実施

**理由**: エコマップ作成は頻繁に実行される処理ではない（1日数回程度）

## Migration Plan

このプロポーザルは新規機能追加のため、マイグレーションは不要です。

### ロールアウト手順
1. 開発環境でのテスト
2. サンプルデータでの動作確認
3. ドキュメント作成
4. ZIPパッケージ作成
5. Claude Desktopでの動作検証
6. リリース

### ロールバック戦略
- 問題が発生した場合、旧バージョンのZIPファイルを再アップロード
- Git履歴から以前のコミットにロールバック可能

## Open Questions

1. **Q**: 対話モードで収集したデータをExcelファイルとして保存する機能は必要か？
   **A**: 将来的な拡張として検討。初期バージョンではJSON/HTML出力のみ。

2. **Q**: 複数ケースの一括処理は対応すべきか？
   **A**: Non-Goalとして、将来的な拡張に残す。

3. **Q**: Claude Desktop以外のプラットフォーム（Claude API等）でも動作させるべきか？
   **A**: 将来的な拡張として検討。初期バージョンはClaude Desktop専用。

## Success Metrics

実装完了後、以下の指標で成功を測定：

1. **機能性**: すべてのテストケースが通過
2. **ユーザビリティ**: 対話モードで5分以内にエコマップ作成可能
3. **互換性**: 既存のExcelテンプレートで引き続き動作
4. **インストール**: uvを使用して5分以内にセットアップ完了
5. **ドキュメント**: README_INSTALLATION.mdの手順に従って、初心者がインストール可能
