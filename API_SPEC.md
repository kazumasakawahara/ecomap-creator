# エコマップ作成スキル API仕様書

**バージョン**: 1.0.0  
**最終更新**: 2025年10月21日  
**対象**: 開発者・APIユーザー

---

## 📋 目次

1. [概要](#概要)
2. [コマンドラインインターフェース](#コマンドラインインターフェース)
3. [Pythonインターフェース](#pythonインターフェース)
4. [データ構造](#データ構造)
5. [エラーコード](#エラーコード)
6. [使用例](#使用例)

---

## 概要

エコマップ作成スキルは、Excelファイルから支援情報を読み込み、JSONおよびHTMLファイルとして出力します。

### 主要機能

- Excelファイル読み込み
- データ検証
- 日付変換（元号→西暦）
- ノード・リレーション生成
- JSON出力
- HTML可視化

### 入出力

**入力**:
- Excelファイル（.xlsx）
- CSVファイル（.csv）※オプション

**出力**:
- JSONファイル（構造化データ）
- HTMLファイル（可視化エコマップ）

---

## コマンドラインインターフェース

### 基本的な使用方法

```bash
python3 ecomap_creator.py [オプション] 入力ファイル
```

### オプション

| オプション | 短縮形 | 説明 | デフォルト |
|-----------|-------|------|-----------|
| `--output` | `-o` | 出力ディレクトリ | `outputs/` |
| `--debug` | `-d` | デバッグモード | False |
| `--quiet` | `-q` | 静音モード | False |
| `--no-html` | | HTML生成をスキップ | False |
| `--visualization` | `-v` | 可視化ライブラリ | `d3` |
| `--version` | | バージョン表示 | - |
| `--help` | `-h` | ヘルプ表示 | - |

### 使用例

#### 例1: 基本的な使用

```bash
python3 ecomap_creator.py sample_case_01.xlsx
```

**出力**:
```
[INFO] Excelファイルを読み込んでいます: sample_case_01.xlsx
[INFO] データを検証しています...
[INFO] データを変換しています...
[INFO] ノードを生成しています...
[INFO] リレーションを生成しています...
[INFO] JSONファイルを生成しています: outputs/佐藤健太_ecomap.json
[INFO] HTMLファイルを生成しています: outputs/佐藤健太_ecomap.html
[SUCCESS] エコマップを作成しました！
```

#### 例2: 出力先を指定

```bash
python3 ecomap_creator.py sample_case_02.xlsx --output ~/Documents/ecomaps/
```

#### 例3: デバッグモード

```bash
python3 ecomap_creator.py sample_case_03.xlsx --debug
```

**出力** (詳細なログ):
```
[DEBUG] openpyxlバージョン: 3.1.5
[DEBUG] Excelファイルを開いています...
[DEBUG] シート「本人情報」を読み込んでいます...
[DEBUG] 氏名: 鈴木正雄
[DEBUG] 生年月日: 1955-03-15
[DEBUG] シート「家族情報」を読み込んでいます...
[DEBUG] 家族メンバー数: 2
...
```

#### 例4: Cytoscape.jsで可視化

```bash
python3 ecomap_creator.py sample_case_01.xlsx --visualization cytoscape
```

#### 例5: JSONのみ生成（HTML不要）

```bash
python3 ecomap_creator.py sample_case_02.xlsx --no-html
```

### 終了コード

| コード | 説明 |
|-------|------|
| 0 | 正常終了 |
| 1 | ファイルが見つからない |
| 2 | データ検証エラー |
| 3 | 日付変換エラー |
| 4 | ノード生成エラー |
| 5 | ファイル出力エラー |
| 99 | その他のエラー |

---

## Pythonインターフェース

### EcomapCreatorクラス

#### 初期化

```python
from ecomap_creator import EcomapCreator

creator = EcomapCreator(
    input_file: str,
    output_dir: str = "outputs",
    visualization: str = "d3",
    debug: bool = False
)
```

**パラメータ**:

| パラメータ | 型 | 必須 | 説明 |
|-----------|---|------|------|
| `input_file` | str | ✓ | 入力Excelファイルパス |
| `output_dir` | str | | 出力ディレクトリ（デフォルト: "outputs"）|
| `visualization` | str | | 可視化ライブラリ（"d3" or "cytoscape"）|
| `debug` | bool | | デバッグモード |

#### メソッド

##### run()

エコマップ作成のメイン処理を実行します。

```python
json_path, html_path = creator.run()
```

**戻り値**:
- `tuple[str, str]`: (JSONファイルパス, HTMLファイルパス)

**例外**:
- `FileNotFoundError`: 入力ファイルが見つからない
- `ValidationError`: データ検証エラー
- `ConversionError`: データ変換エラー
- `GenerationError`: ファイル生成エラー

**使用例**:

```python
from ecomap_creator import EcomapCreator

try:
    creator = EcomapCreator("sample_case_01.xlsx")
    json_path, html_path = creator.run()
    print(f"JSON: {json_path}")
    print(f"HTML: {html_path}")
except ValidationError as e:
    print(f"データエラー: {e}")
except Exception as e:
    print(f"エラー: {e}")
```

##### load_excel()

Excelファイルを読み込みます（低レベルAPI）。

```python
data = creator.load_excel()
```

**戻り値**:
- `dict`: 読み込んだデータ

**使用例**:

```python
creator = EcomapCreator("sample_case_01.xlsx")
data = creator.load_excel()
print(data["person"]["name"])  # "佐藤健太"
```

##### validate_data()

データを検証します（低レベルAPI）。

```python
errors = creator.validate_data(data)
```

**パラメータ**:
- `data` (dict): 検証するデータ

**戻り値**:
- `list[str]`: エラーメッセージのリスト（空ならエラーなし）

**使用例**:

```python
data = creator.load_excel()
errors = creator.validate_data(data)

if errors:
    for error in errors:
        print(f"エラー: {error}")
else:
    print("データは有効です")
```

##### convert_dates()

日付を変換します（低レベルAPI）。

```python
converted_data = creator.convert_dates(data)
```

**パラメータ**:
- `data` (dict): 変換するデータ

**戻り値**:
- `dict`: 変換後のデータ

**使用例**:

```python
data = creator.load_excel()
converted_data = creator.convert_dates(data)
print(converted_data["person"]["age"])  # 4
```

##### generate_json()

JSONファイルを生成します（低レベルAPI）。

```python
json_path = creator.generate_json(nodes, relations, metadata)
```

**パラメータ**:
- `nodes` (list[dict]): ノードのリスト
- `relations` (list[dict]): リレーションのリスト
- `metadata` (dict): メタデータ

**戻り値**:
- `str`: 生成されたJSONファイルパス

##### generate_html()

HTMLファイルを生成します（低レベルAPI）。

```python
html_path = creator.generate_html(json_data, person_name)
```

**パラメータ**:
- `json_data` (dict): JSONデータ
- `person_name` (str): 本人氏名

**戻り値**:
- `str`: 生成されたHTMLファイルパス

### ユーティリティクラス

#### DateConverter

```python
from modules.date_converter import DateConverter

converter = DateConverter()
```

##### convert_wareki_to_seireki()

元号を西暦に変換します。

```python
seireki = DateConverter.convert_wareki_to_seireki("令和5年4月1日")
# "2023-04-01"
```

**パラメータ**:
- `date_str` (str): 元号形式の日付

**戻り値**:
- `str`: 西暦形式の日付（YYYY-MM-DD）

**サポートする元号**:
- 令和（2018 + ○年）
- 平成（1988 + ○年）
- 昭和（1925 + ○年）
- 大正（1911 + ○年）
- 明治（1867 + ○年）

##### calculate_age()

年齢を計算します。

```python
age = DateConverter.calculate_age("2021-04-15")
# 4
```

**パラメータ**:
- `birth_date` (str): 生年月日（YYYY-MM-DD）

**戻り値**:
- `int`: 年齢

##### normalize_date()

日付を正規化します（元号→西暦、形式統一）。

```python
normalized = DateConverter.normalize_date("令和5年4月1日")
# "2023-04-01"

normalized = DateConverter.normalize_date("2023/4/1")
# "2023-04-01"
```

**パラメータ**:
- `date_str` (str): 日付文字列

**戻り値**:
- `str`: 正規化された日付（YYYY-MM-DD）

#### Validator

```python
from modules.validator import Validator

validator = Validator()
```

##### validate_required_fields()

必須フィールドを検証します。

```python
errors = Validator.validate_required_fields(
    data={"name": "山田太郎", "age": 30},
    required=["name", "age", "address"]
)
# ["addressが入力されていません"]
```

**パラメータ**:
- `data` (dict): 検証するデータ
- `required` (list[str]): 必須フィールドのリスト

**戻り値**:
- `list[str]`: エラーメッセージのリスト

##### validate_date_format()

日付形式を検証します。

```python
is_valid = Validator.validate_date_format("2023-04-01")  # True
is_valid = Validator.validate_date_format("2023/04/01")  # True
is_valid = Validator.validate_date_format("令和5年4月1日")  # True
is_valid = Validator.validate_date_format("invalid")     # False
```

**パラメータ**:
- `date_str` (str): 日付文字列

**戻り値**:
- `bool`: 有効な形式ならTrue

##### validate_enum_value()

列挙型値を検証します。

```python
is_valid = Validator.validate_enum_value(
    value="男",
    allowed=["男", "女", "その他"]
)  # True
```

**パラメータ**:
- `value` (str): 検証する値
- `allowed` (list[str]): 許可された値のリスト

**戻り値**:
- `bool`: 許可された値ならTrue

---

## データ構造

### 入力データ形式（Excelから読み込み後）

```python
{
    "person": {
        "name": str,              # 氏名（必須）
        "birth_date": str,        # 生年月日（必須）
        "gender": str,            # 性別（必須）
        "address": str,           # 住所
        "postal_code": str,       # 郵便番号
        "phone": str,             # 電話番号
        "emergency_contact": str, # 緊急連絡先
        "notes": str              # 備考
    },
    "family": [
        {
            "name": str,           # 氏名（必須）
            "relation": str,       # 続柄（必須）
            "birth_date": str,     # 生年月日
            "gender": str,         # 性別
            "living_together": str, # 同居（必須）
            "primary_caregiver": str, # 主介護者
            "address": str,        # 住所
            "phone": str,          # 電話番号
            "notes": str           # 備考
        }
    ],
    "notebooks": [
        {
            "type": str,           # 手帳種別（必須）
            "grade": str,          # 等級・判定（必須）
            "number": str,         # 手帳番号
            "issue_date": str,     # 交付日（必須）
            "expiry_date": str,    # 有効期限
            "issuing_authority": str, # 交付自治体（必須）
            "status": str,         # 状態（必須）
            "notes": str           # 備考
        }
    ],
    "support_levels": [
        {
            "level": int,          # 支援区分（必須）
            "decision_date": str,  # 決定日（必須）
            "expiry_date": str,    # 有効期限
            "deciding_authority": str, # 決定自治体（必須）
            "assessor": str,       # 認定調査員
            "status": str,         # 状態（必須）
            "notes": str           # 備考
        }
    ],
    "diagnoses": [
        {
            "name": str,           # 診断名（必須）
            "icd10_code": str,     # ICD-10コード
            "diagnosis_date": str, # 診断日
            "doctor": str,         # 診断医
            "institution": str,    # 医療機関
            "status": str,         # 状態（必須）
            "notes": str           # 備考
        }
    ],
    "legal_guardians": [
        {
            "name": str,           # 後見人氏名（必須）
            "type": str,           # 後見類型（必須）
            "category": str,       # 後見人種別（必須）
            "profession": str,     # 専門職種
            "start_date": str,     # 開始日（必須）
            "authority": str,      # 権限範囲
            "contact": str,        # 連絡先
            "notes": str           # 備考
        }
    ],
    "consultation_supports": [
        {
            "office_name": str,    # 事業所名（必須）
            "office_number": str,  # 事業所番号
            "support_type": str,   # 支援種別（必須）
            "specialist": str,     # 担当専門員（必須）
            "address": str,        # 住所
            "phone": str,          # 電話番号
            "contract_date": str,  # 契約日
            "notes": str           # 備考
        }
    ],
    "service_plans": [
        {
            "plan_number": str,    # 計画番号
            "creation_date": str,  # 作成日（必須）
            "last_monitoring_date": str, # 前回モニタリング日
            "next_monitoring_date": str, # 次回モニタリング予定日
            "status": str,         # 状態（必須）
            "notes": str           # 備考
        }
    ],
    "service_contracts": [
        {
            "service_type": str,   # サービス種別（必須）
            "office_name": str,    # 事業所名（必須）
            "office_number": str,  # 事業所番号
            "manager": str,        # サービス管理責任者
            "address": str,        # 住所
            "phone": str,          # 電話番号
            "contract_date": str,  # 契約日（必須）
            "frequency": str,      # 利用頻度
            "days": str,           # 利用曜日
            "status": str,         # 状態（必須）
            "notes": str           # 備考
        }
    ],
    "medical_institutions": [
        {
            "name": str,           # 医療機関名（必須）
            "department": str,     # 診療科（必須）
            "doctor": str,         # 担当医
            "primary_doctor": str, # 主治医
            "address": str,        # 住所
            "phone": str,          # 電話番号
            "start_date": str,     # 通院開始日
            "frequency": str,      # 通院頻度
            "treatment": str,      # 治療内容
            "medications": str,    # 処方薬
            "notes": str           # 備考
        }
    ]
}
```

### 出力データ形式（JSON）

```python
{
    "person": {
        "id": str,              # UUID v4
        "name": str,            # 氏名
        "birth_date": str,      # 生年月日（YYYY-MM-DD）
        "age": int,             # 年齢
        "gender": str,          # 性別
        "properties": dict      # その他のプロパティ
    },
    "nodes": [
        {
            "id": str,          # UUID v4
            "type": str,        # ノードタイプ
            "name": str,        # ノード名
            "properties": dict, # プロパティ
            "display": {
                "color": str,   # 色
                "size": str,    # サイズ
                "shape": str,   # 形状
                "label": str,   # ラベル
                "icon": str     # アイコン（オプション）
            },
            "layer": str,       # レイヤー名
            "is_default_visible": bool, # デフォルト表示
            "created_at": str   # 作成日時（ISO 8601）
        }
    ],
    "relations": [
        {
            "id": str,          # UUID v4
            "type": str,        # リレーションタイプ
            "source_id": str,   # 始点ノードID
            "target_id": str,   # 終点ノードID
            "properties": dict, # プロパティ
            "direction": str,   # 方向（"directed" or "undirected"）
            "display": {
                "line_style": str, # 線のスタイル
                "line_width": int, # 線の幅
                "color": str,   # 色
                "arrow": bool,  # 矢印の有無
                "label": str    # ラベル（オプション）
            },
            "layer": str,       # レイヤー名
            "created_at": str   # 作成日時（ISO 8601）
        }
    ],
    "metadata": {
        "created_at": str,      # 作成日時（ISO 8601）
        "created_by": str,      # 作成者（システム名）
        "version": str,         # バージョン番号
        "schema_version": str,  # スキーマバージョン
        "source_file": str,     # 元ファイル名
        "node_count": int,      # ノード数
        "relation_count": int,  # リレーション数
        "person_name": str,     # 本人氏名
        "person_age": int       # 本人年齢
    }
}
```

---

## エラーコード

### エラークラス階層

```
Exception
├── EcomapError (基底クラス)
│   ├── FileError
│   │   ├── FileNotFoundError
│   │   └── FilePermissionError
│   ├── ValidationError
│   │   ├── RequiredFieldError
│   │   ├── DateFormatError
│   │   └── EnumValueError
│   ├── ConversionError
│   │   ├── DateConversionError
│   │   └── EncodingError
│   └── GenerationError
│       ├── NodeGenerationError
│       ├── RelationGenerationError
│       └── OutputGenerationError
```

### エラーメッセージ一覧

| エラーコード | エラークラス | メッセージ | 原因 | 対処法 |
|-------------|-------------|-----------|------|--------|
| E001 | FileNotFoundError | ファイルが見つかりません | 指定されたファイルが存在しない | ファイルパスを確認 |
| E002 | FilePermissionError | ファイルにアクセスできません | ファイルの権限がない | ファイルの権限を確認 |
| E101 | RequiredFieldError | 必須フィールドが入力されていません | 必須項目が未入力 | 必須項目を入力 |
| E102 | DateFormatError | 日付形式が不正です | 日付の形式が間違っている | 正しい形式で入力 |
| E103 | EnumValueError | 許可されていない値です | 列挙型の値が不正 | 許可された値を入力 |
| E201 | DateConversionError | 日付変換に失敗しました | 日付の変換エラー | 日付形式を確認 |
| E202 | EncodingError | 文字エンコードエラー | 文字コードの問題 | UTF-8で保存 |
| E301 | NodeGenerationError | ノード生成に失敗しました | ノード生成エラー | データを確認 |
| E302 | RelationGenerationError | リレーション生成に失敗しました | リレーション生成エラー | ノードIDを確認 |
| E303 | OutputGenerationError | 出力ファイル生成に失敗しました | ファイル出力エラー | ディスク容量を確認 |

### エラーハンドリング例

```python
from ecomap_creator import EcomapCreator
from ecomap_creator.exceptions import (
    FileNotFoundError,
    ValidationError,
    ConversionError,
    GenerationError
)

try:
    creator = EcomapCreator("sample_case_01.xlsx")
    json_path, html_path = creator.run()
    print(f"成功: {json_path}")

except FileNotFoundError as e:
    print(f"ファイルエラー: {e}")
    print(f"エラーコード: {e.error_code}")
    # E001

except ValidationError as e:
    print(f"データエラー: {e}")
    print(f"エラーコード: {e.error_code}")
    print(f"エラー箇所: {e.field_name}")
    # E101, E102, E103

except ConversionError as e:
    print(f"変換エラー: {e}")
    print(f"エラーコード: {e.error_code}")
    # E201, E202

except GenerationError as e:
    print(f"生成エラー: {e}")
    print(f"エラーコード: {e.error_code}")
    # E301, E302, E303

except Exception as e:
    print(f"予期しないエラー: {e}")
```

---

## 使用例

### 例1: 基本的な使用（コマンドライン）

```bash
# 1. サンプルテンプレートを作成
python3 template_creator.py

# 2. サンプルデータを作成
python3 sample_data_creator.py

# 3. エコマップを生成
python3 ecomap_creator.py samples/sample_case_01.xlsx

# 4. 生成されたHTMLを開く
open outputs/佐藤健太_ecomap.html
```

### 例2: Pythonスクリプトから使用

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ecomap_creator import EcomapCreator
import sys

def main():
    # 入力ファイルを指定
    input_file = "samples/sample_case_02.xlsx"
    
    # EcomapCreatorを初期化
    creator = EcomapCreator(
        input_file=input_file,
        output_dir="outputs",
        visualization="cytoscape",  # Cytoscape.jsを使用
        debug=True                   # デバッグモード
    )
    
    try:
        # エコマップを生成
        json_path, html_path = creator.run()
        
        # 成功メッセージ
        print(f"✓ JSONファイル: {json_path}")
        print(f"✓ HTMLファイル: {html_path}")
        
        return 0
        
    except Exception as e:
        print(f"✗ エラー: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

### 例3: 低レベルAPIの使用

```python
from ecomap_creator import EcomapCreator

# 初期化
creator = EcomapCreator("samples/sample_case_03.xlsx", debug=True)

# ステップ1: Excelファイル読み込み
print("📖 Excelファイルを読み込んでいます...")
data = creator.load_excel()
print(f"本人: {data['person']['name']}")

# ステップ2: データ検証
print("✓ データを検証しています...")
errors = creator.validate_data(data)
if errors:
    for error in errors:
        print(f"  エラー: {error}")
    exit(1)

# ステップ3: 日付変換
print("📅 日付を変換しています...")
converted_data = creator.convert_dates(data)
print(f"年齢: {converted_data['person']['age']}歳")

# ステップ4: ノード生成
print("🔵 ノードを生成しています...")
nodes = creator._generate_nodes(converted_data)
print(f"ノード数: {len(nodes)}")

# ステップ5: リレーション生成
print("🔗 リレーションを生成しています...")
relations = creator._generate_relations(nodes)
print(f"リレーション数: {len(relations)}")

# ステップ6: メタデータ生成
metadata = {
    "created_at": "2025-10-21T12:00:00+09:00",
    "created_by": "ecomap-creator v1.0.0",
    "version": "1.0.0",
    "schema_version": "1.0.0",
    "source_file": "sample_case_03.xlsx",
    "node_count": len(nodes),
    "relation_count": len(relations),
    "person_name": converted_data["person"]["name"],
    "person_age": converted_data["person"]["age"]
}

# ステップ7: JSON生成
print("💾 JSONファイルを生成しています...")
json_path = creator.generate_json(nodes, relations, metadata)
print(f"JSONファイル: {json_path}")

# ステップ8: HTML生成
print("🌐 HTMLファイルを生成しています...")
json_data = {
    "person": converted_data["person"],
    "nodes": nodes,
    "relations": relations,
    "metadata": metadata
}
html_path = creator.generate_html(json_data, converted_data["person"]["name"])
print(f"HTMLファイル: {html_path}")

print("✓ 完了！")
```

### 例4: カスタムバリデーション

```python
from ecomap_creator import EcomapCreator
from modules.validator import Validator

# カスタムバリデーション関数
def validate_kitakyushu_city(data):
    """北九州市周辺の自治体のみ許可"""
    allowed_cities = [
        "北九州市", "下関市", "中間市", "遠賀郡",
        "苅田町", "行橋市", "豊前市"
    ]
    
    errors = []
    
    # 手帳の交付自治体をチェック
    for notebook in data.get("notebooks", []):
        authority = notebook.get("issuing_authority", "")
        if not any(city in authority for city in allowed_cities):
            errors.append(
                f"手帳の交付自治体が対象地域外です: {authority}"
            )
    
    # 支援区分の決定自治体をチェック
    for level in data.get("support_levels", []):
        authority = level.get("deciding_authority", "")
        if not any(city in authority for city in allowed_cities):
            errors.append(
                f"支援区分の決定自治体が対象地域外です: {authority}"
            )
    
    return errors

# 使用例
creator = EcomapCreator("input.xlsx")
data = creator.load_excel()

# 標準バリデーション
errors = creator.validate_data(data)

# カスタムバリデーション
custom_errors = validate_kitakyushu_city(data)
errors.extend(custom_errors)

if errors:
    for error in errors:
        print(f"エラー: {error}")
else:
    json_path, html_path = creator.run()
    print("成功！")
```

### 例5: バッチ処理

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
from ecomap_creator import EcomapCreator
from pathlib import Path

def batch_process(input_dir, output_dir):
    """複数のExcelファイルを一括処理"""
    
    # Excelファイルを検索
    excel_files = glob.glob(f"{input_dir}/*.xlsx")
    
    print(f"📁 {len(excel_files)}個のファイルを処理します")
    
    success_count = 0
    error_count = 0
    
    for excel_file in excel_files:
        file_name = Path(excel_file).name
        print(f"\n処理中: {file_name}")
        
        try:
            creator = EcomapCreator(
                input_file=excel_file,
                output_dir=output_dir,
                quiet=True  # 静音モード
            )
            
            json_path, html_path = creator.run()
            print(f"  ✓ 成功")
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ エラー: {e}")
            error_count += 1
    
    # 結果サマリー
    print(f"\n{'='*50}")
    print(f"処理完了")
    print(f"  成功: {success_count}件")
    print(f"  失敗: {error_count}件")
    print(f"{'='*50}")

if __name__ == "__main__":
    batch_process(
        input_dir="inputs",
        output_dir="outputs"
    )
```

---

## 付録

### 設定ファイル（config.json）

将来的な拡張として、設定ファイルをサポート予定です。

```json
{
    "version": "1.0.0",
    "output": {
        "directory": "outputs",
        "json_indent": 2,
        "html_minify": false
    },
    "visualization": {
        "library": "d3",
        "default_layers": [
            "person",
            "family",
            "notebooks",
            "support_levels",
            "service_plans",
            "service_contracts"
        ],
        "colors": {
            "Person": "orange",
            "Family": "red",
            "RyoikuNotebook": "darkred",
            "MentalHealthNotebook": "darkgreen",
            "PhysicalDisabilityNotebook": "darkblue"
        }
    },
    "validation": {
        "strict_mode": false,
        "custom_rules": []
    },
    "logging": {
        "level": "INFO",
        "file": "ecomap.log",
        "console": true
    }
}
```

### ログ出力例

```
2025-10-21 12:00:00,123 - INFO - ecomap_creator - Starting ecomap creation
2025-10-21 12:00:00,234 - INFO - excel_reader - Loading Excel file: sample_case_01.xlsx
2025-10-21 12:00:00,345 - DEBUG - excel_reader - Reading sheet: 本人情報
2025-10-21 12:00:00,456 - DEBUG - excel_reader - Found person: 佐藤健太
2025-10-21 12:00:00,567 - INFO - validator - Validating data...
2025-10-21 12:00:00,678 - INFO - date_converter - Converting dates...
2025-10-21 12:00:00,789 - DEBUG - date_converter - Birth date: 2021-04-15 (4 years old)
2025-10-21 12:00:00,890 - INFO - node_generator - Generating nodes...
2025-10-21 12:00:01,001 - DEBUG - node_generator - Generated 17 nodes
2025-10-21 12:00:01,112 - INFO - relation_generator - Generating relations...
2025-10-21 12:00:01,223 - DEBUG - relation_generator - Generated 17 relations
2025-10-21 12:00:01,334 - INFO - output - Writing JSON file: outputs/佐藤健太_ecomap.json
2025-10-21 12:00:01,445 - INFO - html_generator - Generating HTML file...
2025-10-21 12:00:01,556 - INFO - output - Writing HTML file: outputs/佐藤健太_ecomap.html
2025-10-21 12:00:01,667 - INFO - ecomap_creator - Ecomap creation completed successfully
```

---

**以上、エコマップ作成スキルのAPI仕様書でした。**
