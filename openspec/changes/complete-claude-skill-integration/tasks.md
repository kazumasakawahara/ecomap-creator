# Implementation Tasks

## 1. SKILL.md改善
- [ ] 1.1 YAML frontmatterを追加（name, description, version, dependencies）
- [ ] 1.2 対話型モードの使用方法セクションを追加
- [ ] 1.3 uvを使用したインストール手順を追加
- [ ] 1.4 Claude Desktopでの使用例を追加

## 2. uv統合
- [ ] 2.1 `pyproject.toml`を作成（PEP 621準拠）
- [ ] 2.2 プロジェクトメタデータを定義（name, version, description, authors等）
- [ ] 2.3 依存関係を定義（openpyxl等）
- [ ] 2.4 スクリプトエントリポイントを定義（ecomap-creator）
- [ ] 2.5 uv lockファイルを生成
- [ ] 2.6 requirements.txtとの互換性を維持

## 3. 対話型エンジンの実装
- [ ] 3.1 `modules/interactive_dialog.py`を作成
- [ ] 3.2 `InteractiveDialogEngine`クラスを実装
  - [ ] 3.2.1 `start_session()` - セッション開始
  - [ ] 3.2.2 `collect_person_info()` - 本人情報の収集
  - [ ] 3.2.3 `collect_family_info()` - 家族情報の収集
  - [ ] 3.2.4 `collect_notebook_info()` - 手帳情報の収集
  - [ ] 3.2.5 `collect_support_level_info()` - 支援区分情報の収集
  - [ ] 3.2.6 `collect_service_info()` - サービス情報の収集
  - [ ] 3.2.7 `collect_medical_info()` - 医療情報の収集
  - [ ] 3.2.8 `validate_input()` - 入力データの検証
  - [ ] 3.2.9 `provide_feedback()` - フィードバック提供
- [ ] 3.3 質問テンプレートの定義
- [ ] 3.4 入力パーサーの実装（日付、選択肢等）
- [ ] 3.5 既存のValidatorクラスとの統合

## 4. メインスクリプトの完成
- [ ] 4.1 `ecomap_creator.py`の`EcomapCreator`クラスを完成
  - [ ] 4.1.1 `__init__()`の実装
  - [ ] 4.1.2 `run()`メソッドの実装
  - [ ] 4.1.3 モード判定ロジック（対話 vs ファイル）
- [ ] 4.2 対話モードの実装
  - [ ] 4.2.1 `InteractiveDialogEngine`の統合
  - [ ] 4.2.2 収集データのJSON化
- [ ] 4.3 ファイルモードの実装
  - [ ] 4.3.1 既存モジュールの統合
  - [ ] 4.3.2 `_load_excel()`の実装
  - [ ] 4.3.3 `_validate_data()`の実装
  - [ ] 4.3.4 `_convert_dates()`の実装
  - [ ] 4.3.5 `_generate_nodes()`の実装
  - [ ] 4.3.6 `_generate_relations()`の実装
  - [ ] 4.3.7 `_generate_json()`の実装
  - [ ] 4.3.8 `_generate_html()`の実装
- [ ] 4.4 エラーハンドリングの実装
- [ ] 4.5 ロギングの実装
- [ ] 4.6 コマンドライン引数パーサーの実装（argparse）

## 5. パッケージング
- [ ] 5.1 `package.sh`スクリプトを作成（ZIP生成自動化）
- [ ] 5.2 ZIPに含めるファイルのリストを定義
- [ ] 5.3 除外ファイルの定義（__pycache__, .pyc等）
- [ ] 5.4 バージョン番号の自動埋め込み

## 6. ドキュメント更新
- [ ] 6.1 `README.md`を更新
  - [ ] 6.1.1 uvインストール手順を追加
  - [ ] 6.1.2 Claude Desktopでの使用方法を追加
- [ ] 6.2 `README_INSTALLATION.md`を作成
  - [ ] 6.2.1 uvのインストール方法
  - [ ] 6.2.2 スキルのインストール方法
  - [ ] 6.2.3 Claude Desktopへのアップロード方法
  - [ ] 6.2.4 トラブルシューティング
- [ ] 6.3 `CHANGELOG.md`を作成

## 7. テストとバリデーション
- [ ] 7.1 対話モードのテスト
  - [ ] 7.1.1 本人情報の収集テスト
  - [ ] 7.1.2 家族情報の収集テスト
  - [ ] 7.1.3 手帳情報の収集テスト
  - [ ] 7.1.4 バリデーションエラーのテスト
- [ ] 7.2 ファイルモードのテスト
  - [ ] 7.2.1 サンプル1（若年層）でのテスト
  - [ ] 7.2.2 サンプル2（中年層）でのテスト
  - [ ] 7.2.3 サンプル3（高齢層）でのテスト
- [ ] 7.3 uvコマンドでの実行テスト
- [ ] 7.4 ZIPパッケージの検証
- [ ] 7.5 Claude Desktopでの動作確認

## 8. クリーンアップ
- [ ] 8.1 不要なファイルの削除
- [ ] 8.2 コードフォーマットの統一
- [ ] 8.3 型ヒントの追加（Python 3.9+）
- [ ] 8.4 docstringの追加（Google形式）
- [ ] 8.5 ライセンス情報の確認

## Dependencies

- タスク3（対話型エンジン）→ タスク4.2（対話モード実装）
- タスク2（uv統合）→ タスク5（パッケージング）
- タスク4（メインスクリプト）→ タスク7（テスト）
- タスク1-4 → タスク6（ドキュメント）

## Estimated Timeline

- タスク1: 0.5時間
- タスク2: 1時間
- タスク3: 3時間
- タスク4: 4時間
- タスク5: 1時間
- タスク6: 2時間
- タスク7: 2時間
- タスク8: 1時間

**合計**: 約14.5時間
