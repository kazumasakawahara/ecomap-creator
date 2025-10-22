# 📘 エコマップデータ変換ルール定義書

**作成日**: 2025年10月21日  
**バージョン**: 1.0.0

---

## 📑 目次

1. [日付変換ルール](#日付変換ルール)
2. [年齢自動計算](#年齢自動計算)
3. [データ検証ルール](#データ検証ルール)
4. [ID生成ルール](#id生成ルール)
5. [表示設定の自動付与](#表示設定の自動付与)
6. [エラーハンドリング](#エラーハンドリング)

---

## 🗓️ 日付変換ルール

### **1. 基本方針**
- **入力**: 西暦または元号（和暦）
- **出力**: ISO 8601形式の西暦（YYYY-MM-DD）
- **目的**: システム内で統一的な日付管理

### **2. 元号変換テーブル**

| 元号 | 開始年 | 計算式 | 例 |
|------|--------|--------|-----|
| 令和 | 2019年 | 2018 + 令和年 | 令和7年 → 2025年 |
| 平成 | 1989年 | 1988 + 平成年 | 平成30年 → 2018年 |
| 昭和 | 1926年 | 1925 + 昭和年 | 昭和60年 → 1985年 |
| 大正 | 1912年 | 1911 + 大正年 | 大正15年 → 1926年 |
| 明治 | 1868年 | 1867 + 明治年 | 明治45年 → 1912年 |

### **3. 認識パターン**

Excelやテキストから以下のパターンを自動認識します：

#### パターン1: 元号形式
```
令和7年4月1日   → 2025-04-01
平成30年12月25日 → 2018-12-25
昭和60年3月15日  → 1985-03-15
```

#### パターン2: 西暦形式
```
2025年4月1日     → 2025-04-01
2025/4/1         → 2025-04-01
2025-04-01       → 2025-04-01（そのまま）
```

#### パターン3: 略式
```
R7.4.1          → 2025-04-01
H30.12.25       → 2018-12-25
S60.3.15        → 1985-03-15
```

### **4. Pythonコード例**

```python
import re
from datetime import datetime

def convert_japanese_date_to_iso(date_string):
    """
    日本の元号表記または西暦表記をISO形式（YYYY-MM-DD）に変換
    
    引数:
        date_string (str): 日付文字列
        
    戻り値:
        str: ISO形式の日付文字列、または変換失敗時は元の文字列
    """
    
    # 既にISO形式（YYYY-MM-DD）の場合はそのまま返す
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_string):
        return date_string
    
    # 元号変換テーブル
    era_map = {
        '令和': 2018, 'R': 2018,
        '平成': 1988, 'H': 1988,
        '昭和': 1925, 'S': 1925,
        '大正': 1911, 'T': 1911,
        '明治': 1867, 'M': 1867
    }
    
    # パターン1: 令和7年4月1日
    match = re.match(r'(令和|平成|昭和|大正|明治)(\d+)年(\d+)月(\d+)日', date_string)
    if match:
        era, year, month, day = match.groups()
        year = era_map[era] + int(year)
        return f"{year:04d}-{int(month):02d}-{int(day):02d}"
    
    # パターン2: R7.4.1
    match = re.match(r'([RHSTM])(\d+)\.(\d+)\.(\d+)', date_string)
    if match:
        era, year, month, day = match.groups()
        year = era_map[era] + int(year)
        return f"{year:04d}-{int(month):02d}-{int(day):02d}"
    
    # パターン3: 2025年4月1日
    match = re.match(r'(\d{4})年(\d+)月(\d+)日', date_string)
    if match:
        year, month, day = match.groups()
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
    
    # パターン4: 2025/4/1
    match = re.match(r'(\d{4})[/-](\d+)[/-](\d+)', date_string)
    if match:
        year, month, day = match.groups()
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
    
    # 変換できない場合は元の文字列を返す
    return date_string
```

### **5. テストケース**

| 入力 | 期待出力 | 説明 |
|------|----------|------|
| 令和7年10月21日 | 2025-10-21 | 元号（フル） |
| R7.10.21 | 2025-10-21 | 元号（略式） |
| 2025年10月21日 | 2025-10-21 | 西暦（フル） |
| 2025/10/21 | 2025-10-21 | 西暦（スラッシュ） |
| 2025-10-21 | 2025-10-21 | 既にISO形式 |

---

## 🎂 年齢自動計算

### **1. 計算式**

生年月日から現在の年齢を自動計算します。

```python
from datetime import date

def calculate_age(birth_date_str):
    """
    生年月日から年齢を計算
    
    引数:
        birth_date_str (str): 生年月日（YYYY-MM-DD形式）
        
    戻り値:
        int: 年齢
    """
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        today = date.today()
        
        # 年齢計算（誕生日前は-1歳）
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
            
        return age
    except:
        return None
```

### **2. 適用箇所**

年齢は以下のノードで自動計算されます：

- **Personノード**: 本人の年齢
- **Familyノード**: 家族メンバーの年齢

### **3. 注意事項**

- 年齢は**計算時点**での年齢です
- Excelに年齢を入力しても無視され、生年月日から自動計算されます
- 生年月日が空欄の場合、年齢は`null`になります

---

## ✅ データ検証ルール

### **1. 必須フィールドチェック**

各ノードタイプで必須フィールドが空欄の場合、エラーとします。

#### Person（本人）
- ✅ 氏名
- ✅ 生年月日
- ✅ 性別

#### Family（家族）
- ✅ 氏名
- ✅ 続柄
- ✅ 同居（〇/×）

#### Notebook（手帳）
- ✅ 手帳種別
- ✅ 等級・判定
- ✅ 交付日
- ✅ 交付自治体
- ✅ 状態

#### SupportLevel（支援区分）
- ✅ 支援区分
- ✅ 決定日
- ✅ 決定自治体
- ✅ 状態

（以下、各ノードタイプの必須フィールドは schema.json の required を参照）

### **2. 形式検証**

#### 日付形式
- ISO 8601形式（YYYY-MM-DD）に統一
- 元号入力の場合は自動変換

#### 郵便番号
- パターン: `123-4567` または `1234567`
- 正規表現: `^[0-9]{3}-?[0-9]{4}$`

#### 事業所番号
- パターン: 10桁の数字
- 正規表現: `^[0-9]{10}$`

#### メールアドレス
- RFC 5322準拠のメールアドレス形式

### **3. 値の範囲検証**

#### 支援区分
- 許容値: `0`, `1`, `2`, `3`, `4`, `5`, `6`, `非該当`

#### 性別
- 許容値: `男`, `女`, `その他`

#### 手帳種別
- 許容値: `療育手帳`, `精神保健福祉手帳`, `身体障害者手帳`

#### 後見類型
- 許容値: `後見`, `保佐`, `補助`, `任意後見`

#### サービス状態
- 許容値: `契約中`, `体験中`, `契約終了`

---

## 🆔 ID生成ルール

### **1. UUID v4の使用**

各ノードとリレーションには一意の識別子（UUID v4）を自動生成します。

```python
import uuid

def generate_node_id(node_type, properties):
    """
    ノードの一意IDを生成
    
    引数:
        node_type (str): ノードタイプ
        properties (dict): ノードプロパティ
        
    戻り値:
        str: UUID v4形式のID
    """
    return str(uuid.uuid4())
```

### **2. ID形式**

```
例: "550e8400-e29b-41d4-a716-446655440000"
```

### **3. 再利用の禁止**

- 同じIDは絶対に再利用しない
- 新しいノード/リレーションには必ず新しいIDを生成

---

## 🎨 表示設定の自動付与

### **1. ノードタイプごとの色設定**

| ノードタイプ | 色（16進数） | アイコン | レイヤー |
|--------------|--------------|----------|----------|
| Person | #FF8C00 | 🧑 | default |
| Family | #DC143C | 👨‍👩‍👧‍👦 | family |
| RyoikuNotebook | #8B0000 | 📕 | default |
| MentalHealthNotebook | #006400 | 📗 | default |
| PhysicalDisabilityNotebook | #00008B | 📘 | default |
| SupportLevel | #800080 | 📊 | default |
| Diagnosis | #00CED1 | 🏥 | medical |
| LegalGuardian | #8B4513 | ⚖️ | default |
| ConsultationSupport | #9370DB | 🟣 | support |
| ConsultationSupportSpecialist | #4169E1 | 👤 | support |
| ServicePlan | #6A5ACD | 📋 | default |
| SupportService | #32CD32 | 🟢 | support |
| ServiceManager | #228B22 | 👤 | support |
| ServiceContract | #3CB371 | 📝 | default |
| MedicalInstitution | #5F9EA0 | 🩺 | medical |
| Doctor | #4682B4 | 👨‍⚕️ | medical |
| Government | #A9A9A9 | 🏛️ | support |
| Medication | #DB7093 | 💊 | medical |

### **2. デフォルト表示の判定**

以下の条件でデフォルト表示を決定します：

#### 常に表示（visible: true）
- Person（本人）
- 有効な手帳（status="有効"）
- 現在の支援区分（status="現在"）
- 成年後見人（存在する場合）
- 最新のサービス等利用計画（status="有効"）
- 契約中の福祉サービス（status="契約中"）

#### 展開時に表示（visible: false）
- 同居していない家族（cohabiting=false）
- 期限切れの手帳（status="期限切れ"）
- 過去の支援区分（status="期限切れ"）
- 診断情報（全て）
- 医療機関情報（全て）
- 処方薬情報（全て）
- 相談支援事業所・専門員
- サービス管理責任者

```python
def determine_default_visibility(node_type, properties):
    """
    ノードのデフォルト表示/非表示を判定
    
    引数:
        node_type (str): ノードタイプ
        properties (dict): ノードプロパティ
        
    戻り値:
        bool: True=デフォルト表示、False=展開時のみ表示
    """
    # 本人は常に表示
    if node_type == "Person":
        return True
    
    # 家族は主介護者または同居のみ表示
    if node_type == "Family":
        return properties.get("primaryCaregiver", False) or properties.get("cohabiting", False)
    
    # 手帳・支援区分は有効なもののみ表示
    if node_type in ["RyoikuNotebook", "MentalHealthNotebook", "PhysicalDisabilityNotebook", "SupportLevel"]:
        return properties.get("status") in ["有効", "現在"]
    
    # 成年後見人は常に表示
    if node_type == "LegalGuardian":
        return True
    
    # サービス等利用計画は有効なもののみ表示
    if node_type == "ServicePlan":
        return properties.get("status") == "有効"
    
    # サービス契約は契約中のみ表示
    if node_type == "ServiceContract":
        return properties.get("status") == "契約中"
    
    # 福祉サービスは契約中のみ表示
    if node_type == "SupportService":
        # 関連するServiceContractのstatusをチェック（実装時）
        return True  # 仮
    
    # その他は展開時のみ表示
    return False
```

---

## ⚠️ エラーハンドリング

### **1. エラーレベル**

| レベル | 説明 | 処理 |
|--------|------|------|
| ERROR | 必須フィールド欠如、形式不正 | 処理中断、エラーメッセージ表示 |
| WARNING | 推奨フィールド欠如、軽微な不整合 | 処理継続、警告メッセージ表示 |
| INFO | 補足情報 | ログ出力のみ |

### **2. エラーメッセージ例**

#### ERROR
```
エラー: 本人情報シートの氏名が入力されていません。
エラー: 手帳情報シート 2行目の交付日が不正な形式です。入力値: "令和XX年"
エラー: サービス利用情報シート 3行目の事業所番号が10桁ではありません。入力値: "123456"
```

#### WARNING
```
警告: 家族情報シート 2行目の生年月日が入力されていません。年齢計算はスキップされます。
警告: 診断情報シートにICD-10コードが入力されていません。
```

#### INFO
```
情報: 元号表記 "令和7年4月1日" を西暦 "2025-04-01" に変換しました。
情報: 年齢を自動計算しました: 35歳（生年月日: 1990-04-01）
```

### **3. エラーハンドリングコード例**

```python
class ValidationError(Exception):
    """検証エラー"""
    pass

def validate_required_field(value, field_name, row_number=None):
    """
    必須フィールドの検証
    
    引数:
        value: 検証する値
        field_name (str): フィールド名
        row_number (int): 行番号（Excelの場合）
        
    戻り値:
        None
        
    例外:
        ValidationError: 値が空の場合
    """
    if not value or str(value).strip() == "":
        location = f" {row_number}行目の" if row_number else ""
        raise ValidationError(f"エラー:{location}{field_name}が入力されていません。")

def validate_date_format(date_string, field_name, row_number=None):
    """
    日付形式の検証
    
    引数:
        date_string (str): 日付文字列
        field_name (str): フィールド名
        row_number (int): 行番号
        
    戻り値:
        str: ISO形式の日付文字列
        
    例外:
        ValidationError: 日付が不正な形式の場合
    """
    converted_date = convert_japanese_date_to_iso(date_string)
    
    # ISO形式に変換できたか確認
    try:
        datetime.strptime(converted_date, '%Y-%m-%d')
        return converted_date
    except:
        location = f" {row_number}行目の" if row_number else ""
        raise ValidationError(
            f"エラー:{location}{field_name}が不正な形式です。入力値: \"{date_string}\""
        )
```

### **4. 処理フロー**

```
1. Excelファイル読み込み
2. シートごとにデータ抽出
3. 各行でバリデーション実行
   ├─ 必須フィールドチェック → エラー時: 例外発生、処理中断
   ├─ 形式検証 → エラー時: 例外発生、処理中断
   └─ 値の範囲検証 → 警告レベル: ログ出力、処理継続
4. データ変換（元号→西暦、年齢計算）
5. ノード・リレーション生成
6. JSON出力
```

---

## 🧪 テストデータ例

### **入力（Excel）**

| 氏名 | 生年月日 | 性別 |
|------|----------|------|
| 佐藤健太 | 令和3年4月1日 | 男 |

### **出力（JSON）**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "Person",
  "properties": {
    "name": "佐藤健太",
    "birthDate": "2021-04-01",
    "age": 4,
    "gender": "男"
  },
  "display": {
    "color": "#FF8C00",
    "icon": "🧑",
    "layer": "default",
    "visible": true
  }
}
```

---

## 📚 参考資料

### **日付処理**
- Python `datetime` モジュール: https://docs.python.org/ja/3/library/datetime.html
- ISO 8601規格: https://ja.wikipedia.org/wiki/ISO_8601

### **正規表現**
- Python `re` モジュール: https://docs.python.org/ja/3/library/re.html
- 正規表現テスター: https://regex101.com/

### **UUID**
- Python `uuid` モジュール: https://docs.python.org/ja/3/library/uuid.html

---

**以上、データ変換ルール定義書です。**  
**次のステップ: サンプルJSON出力の作成**
