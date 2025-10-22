# エコマップ作成スキル（Ecomap Creator）

## 概要
知的障害・精神障害のある方の支援情報を一元管理し、視覚的なエコマップとして表示するClaude Agent Skillです。

## 主な利用者
計画相談支援の担当者（相談支援専門員）

## 使用場面
- ケース会議での情報共有
- サービス等利用計画の作成
- 引き継ぎ資料
- モニタリング

## 対象地域
北九州市および隣接市町村

## 機能
- ✅ **対話モード**: Claude Desktopで自然な会話形式でエコマップ作成
- ✅ **ファイルモード**: Excelファイルから一括読み込み
- ✅ 本人・家族・支援者の関係性を可視化
- ✅ 手帳・支援区分・診断情報の管理
- ✅ 成年後見情報の管理
- ✅ サービス利用状況の可視化
- ✅ 医療機関・処方薬情報の管理
- ✅ 履歴管理（手帳更新、支援区分変更など）
- ✅ レイヤー表示（必要な情報のみ表示）

## インストール

### 必要な環境
- Python 3.9以上
- uv (Python package manager)

### uvのインストール
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### プロジェクトのセットアップ
```bash
# リポジトリのクローン
git clone https://github.com/yourusername/ecomap-creator.git
cd ecomap-creator

# 依存関係のインストール
uv sync

# パッケージングスクリプトの実行権限付与
chmod +x package.sh
```

## 使い方

### 1. Claude Desktop での使用（推奨）

#### パッケージング
```bash
./package.sh
```

このコマンドで `ecomap-creator-v1.0.0.zip` が生成されます。

#### Claude Desktopへのアップロード
1. Claude Desktopを開く
2. Settings → Skills → Upload Skill
3. `ecomap-creator-v1.0.0.zip` を選択してアップロード

#### 対話形式での使用
Claude Desktopで以下のように依頼します：

```
「佐藤健太さんのエコマップを作成してください」
```

Claudeが質問してくるので、順番に答えていきます：
- 本人情報（氏名、生年月日、性別）
- 家族情報
- 手帳情報
- 支援区分
- 診断情報
- 成年後見
- サービス利用状況
- 医療機関

全ての質問に答えると、エコマップが自動生成されます。

### 2. コマンドラインでの使用

#### Excelファイルから生成
```bash
uv run ecomap-creator samples/sample_case_01.xlsx
```

#### 生成されたファイル
- `outputs/<本人名>_ecomap.json` - エコマップデータ（JSON形式）
- `outputs/<本人名>_ecomap.html` - 可視化されたエコマップ（ブラウザで開く）

#### オプション
```bash
uv run ecomap-creator <入力ファイル> [オプション]

オプション:
  -o, --output DIR        出力ディレクトリ（デフォルト: outputs）
  -v, --visualization LIB 可視化ライブラリ（d3/cytoscape、デフォルト: d3）
  -d, --debug            デバッグモード
  -i, --interactive      対話モードで実行
  --version              バージョン表示
```

## ディレクトリ構造
```
ecomap-creator/
├── SKILL.md                    # Claude Skillドキュメント
├── README.md                   # このファイル
├── pyproject.toml              # Python プロジェクト設定
├── uv.lock                     # uvロックファイル
├── package.sh                  # パッケージングスクリプト
├── ecomap_creator.py           # メインスクリプト
├── schema.json                 # JSONスキーマ定義
├── DATA_CONVERSION_RULES.md    # データ変換ルール
├── USAGE_GUIDE.md              # 使用ガイド
├── modules/                    # Pythonモジュール
│   ├── __init__.py
│   ├── excel_reader.py         # Excel読み込み
│   ├── validator.py            # データ検証
│   ├── date_converter.py       # 日付変換
│   ├── node_generator.py       # ノード生成
│   ├── relation_generator.py   # リレーション生成
│   ├── html_generator.py       # HTML生成
│   └── interactive_dialog.py   # 対話エンジン
├── templates/                  # テンプレート
│   ├── template.xlsx           # Excelテンプレート
│   ├── ecomap_d3.html          # D3.js可視化テンプレート
│   └── ecomap_cytoscape.html   # Cytoscape.js可視化テンプレート
├── samples/                    # サンプルデータ
│   ├── sample_case_01.xlsx     # サンプルケース1
│   ├── sample_case_01.json     # サンプルケース1（JSON）
│   ├── sample_case_02.xlsx     # サンプルケース2
│   ├── sample_case_02.json     # サンプルケース2（JSON）
│   ├── sample_case_03.xlsx     # サンプルケース3
│   └── sample_case_03.json     # サンプルケース3（JSON）
└── outputs/                    # 生成されたエコマップ出力先
```

## 開発状況
✅ **バージョン 1.1.0 完成**

### 完了機能
- [x] ディレクトリ構造作成
- [x] エンティティ・リレーション設計
- [x] Excelテンプレート作成
- [x] サンプルデータ作成
- [x] JSONスキーマ確定
- [x] SKILL.md執筆
- [x] Pythonスクリプト実装
- [x] HTML可視化実装（D3.js / Cytoscape.js）
- [x] 対話モード実装
- [x] uv統合
- [x] Claude Skill パッケージング

## 技術仕様

### 依存関係
- Python 3.9+
- openpyxl 3.1.5+ (Excel読み込み)

### データフロー
```
[入力] → [検証] → [変換] → [ノード生成] → [リレーション生成] → [可視化]
  ↓
Excel or 対話
```

### ノードタイプ（18種類）
本人、家族、手帳、支援区分、診断、成年後見人、相談支援事業所、相談支援専門員、サービス等利用計画、サービス契約、福祉サービス事業所、サービス管理責任者、医療機関、医師、処方薬、など

### リレーションタイプ（19種類）
belongs_to_family、has_notebook、has_support_level、has_diagnosis、managed_by_guardian、created_plan、provides_service、prescribed_medication、など

## 詳細ドキュメント
- [SKILL.md](SKILL.md) - Claude Skill使用マニュアル
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - 詳細な使用ガイド
- [DATA_CONVERSION_RULES.md](DATA_CONVERSION_RULES.md) - データ変換ルール

## トラブルシューティング

### uv sync でエラーが出る
```bash
# uvを最新版に更新
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 対話モードが動作しない
対話モードはClaude Desktop経由での使用を想定しています。コマンドラインでの対話は制限されます。

### パッケージングエラー
```bash
# 実行権限を確認
chmod +x package.sh

# 必要なファイルがすべて存在するか確認
ls -la ecomap_creator.py modules/ templates/ samples/
```

## ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

このソフトウェアは教育・医療・福祉目的での使用を想定していますが、MITライセンスの下で自由に使用・改変・配布できます。

---
**バージョン**: 1.1.0
**作成日**: 2025年10月21日
**最終更新**: 2025年10月22日

## 🆕 バージョン 1.1.0 の変更点
- ✅ Excelテンプレート追加（templates/template.xlsx）
- ✅ 対話モードの詳細実装完了（手帳、支援区分、診断、サービス、医療）
- ✅ 基本的なテストコード追加（9/10テスト成功）
- 🔄 対話モードでの実際のデータ収集が可能に
