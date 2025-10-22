# エコマップ作成スキル 技術仕様書

**バージョン**: 1.0.0  
**最終更新**: 2025年10月21日  
**対象**: 開発者・技術担当者

---

## 📋 目次

1. [システムアーキテクチャ](#システムアーキテクチャ)
2. [データフロー](#データフロー)
3. [技術スタック](#技術スタック)
4. [モジュール設計](#モジュール設計)
5. [データモデル](#データモデル)
6. [処理フロー](#処理フロー)
7. [可視化エンジン](#可視化エンジン)
8. [パフォーマンス要件](#パフォーマンス要件)
9. [セキュリティ](#セキュリティ)
10. [拡張性](#拡張性)

---

## システムアーキテクチャ

### 全体構成

```
┌─────────────────────────────────────────────────────────┐
│                     ユーザー                              │
│              (相談支援専門員)                            │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│              入力レイヤー                                 │
│  ┌──────────────┐    ┌──────────────┐                 │
│  │ Excel/CSV    │    │ 対話入力      │                 │
│  │ テンプレート  │    │ (未実装)      │                 │
│  └──────────────┘    └──────────────┘                 │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│             データ変換レイヤー                            │
│  ┌──────────────────────────────────────────────────┐  │
│  │  ecomap_creator.py (メイン処理)                  │  │
│  │  ┌─────────────────┐  ┌──────────────────┐      │  │
│  │  │ Excel読み込み    │  │ データ検証       │      │  │
│  │  └─────────────────┘  └──────────────────┘      │  │
│  │  ┌─────────────────┐  ┌──────────────────┐      │  │
│  │  │ 日付変換        │  │ ID生成           │      │  │
│  │  └─────────────────┘  └──────────────────┘      │  │
│  │  ┌─────────────────┐  ┌──────────────────┐      │  │
│  │  │ ノード生成      │  │ リレーション生成  │      │  │
│  │  └─────────────────┘  └──────────────────┘      │  │
│  └──────────────────────────────────────────────────┘  │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│             データストレージ                              │
│  ┌──────────────┐    ┌──────────────┐                 │
│  │ JSON出力     │    │ スキーマ検証  │                 │
│  │ (構造化)     │    │ (schema.json) │                 │
│  └──────────────┘    └──────────────┘                 │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│             可視化レイヤー                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │  HTML生成エンジン                                 │  │
│  │  ┌─────────────────┐  ┌──────────────────┐      │  │
│  │  │ D3.js/Cytoscape │  │ レイヤー制御     │      │  │
│  │  └─────────────────┘  └──────────────────┘      │  │
│  │  ┌─────────────────┐  ┌──────────────────┐      │  │
│  │  │ インタラクション │  │ ノード詳細表示   │      │  │
│  │  └─────────────────┘  └──────────────────┘      │  │
│  └──────────────────────────────────────────────────┘  │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│              出力レイヤー                                 │
│  ┌──────────────┐    ┌──────────────┐                 │
│  │ HTMLファイル  │    │ JSONファイル  │                 │
│  │ (可視化)     │    │ (データ)      │                 │
│  └──────────────┘    └──────────────┘                 │
└─────────────────────────────────────────────────────────┘
```

### 設計原則

1. **単一責任の原則**: 各モジュールは1つの責任のみを持つ
2. **疎結合**: モジュール間の依存関係を最小化
3. **高凝集**: 関連する機能を1つのモジュールにまとめる
4. **拡張性**: 新しいノードタイプやリレーションを容易に追加可能
5. **保守性**: コードの可読性と保守性を重視

---

## データフロー

### 処理の流れ

```
[Excelファイル]
    │
    ▼
┌─────────────────┐
│ ファイル読み込み │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ データ検証       │
│ - 必須項目確認   │
│ - 形式チェック   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 日付変換         │
│ - 元号→西暦      │
│ - 年齢計算       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ ノード生成       │
│ - 本人ノード     │
│ - 家族ノード     │
│ - 手帳ノード     │
│ - サービスノード │
│ - (18種類)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ リレーション生成 │
│ - 家族関係       │
│ - 契約関係       │
│ - 診断関係       │
│ - (19種類)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 表示設定付与     │
│ - 色            │
│ - サイズ         │
│ - レイヤー       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ スキーマ検証     │
│ - JSON Schema   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ JSON出力         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ HTML生成         │
│ - D3.js/Cytoscape│
│ - レイヤー制御   │
└────────┬────────┘
         │
         ▼
[HTMLファイル]
[JSONファイル]
```

---

## 技術スタック

### バックエンド（Python）

#### 必須ライブラリ

| ライブラリ | バージョン | 用途 |
|-----------|-----------|------|
| Python | 3.7+ | 実行環境 |
| openpyxl | 3.1.5+ | Excel読み込み |
| json | 標準 | JSON処理 |
| csv | 標準 | CSV処理 |
| datetime | 標準 | 日付処理 |
| uuid | 標準 | ID生成 |
| re | 標準 | 正規表現 |
| argparse | 標準 | コマンドライン引数 |
| logging | 標準 | ロギング |

#### 推奨ライブラリ（将来的な拡張）

| ライブラリ | 用途 |
|-----------|------|
| jsonschema | スキーマ検証 |
| pandas | データ分析（オプション）|
| xlrd | 旧形式Excel対応（.xls）|

### フロントエンド（JavaScript/HTML）

#### 可視化ライブラリ

**オプション1: D3.js**
- バージョン: v7.x
- 特徴: 柔軟なカスタマイズ可能
- 利点: 細かい制御が可能、軽量
- 欠点: 学習曲線が高い

**オプション2: Cytoscape.js**
- バージョン: 3.x
- 特徴: Neo4j風のグラフ表示
- 利点: グラフ表示に特化、API豊富
- 欠点: ファイルサイズが大きい

#### UI/UX

| 技術 | 用途 |
|------|------|
| HTML5 | マークアップ |
| CSS3 | スタイリング |
| JavaScript ES6+ | インタラクション |

### 開発環境

| 項目 | 推奨 |
|------|------|
| OS | macOS、Linux、Windows |
| エディタ | VSCode、PyCharm |
| バージョン管理 | Git |
| パッケージ管理 | pip |

---

## モジュール設計

### ecomap_creator.py（メインスクリプト）

#### クラス構造

```python
class EcomapCreator:
    """エコマップ作成のメインクラス"""
    
    def __init__(self, input_file: str, output_dir: str = "outputs"):
        """初期化"""
        
    def run(self) -> tuple[str, str]:
        """メイン処理実行"""
        
    def _load_excel(self) -> dict:
        """Excelファイル読み込み"""
        
    def _validate_data(self, data: dict) -> list[str]:
        """データ検証"""
        
    def _convert_dates(self, data: dict) -> dict:
        """日付変換"""
        
    def _generate_nodes(self, data: dict) -> list[dict]:
        """ノード生成"""
        
    def _generate_relations(self, nodes: list[dict]) -> list[dict]:
        """リレーション生成"""
        
    def _generate_json(self, nodes: list[dict], relations: list[dict]) -> dict:
        """JSON生成"""
        
    def _generate_html(self, json_data: dict, person_name: str) -> str:
        """HTML生成"""
```

#### サブモジュール

**1. ExcelReader**
```python
class ExcelReader:
    """Excel読み込み専用クラス"""
    
    @staticmethod
    def read_sheet(workbook, sheet_name: str) -> list[dict]:
        """シート読み込み"""
        
    @staticmethod
    def extract_person_info(workbook) -> dict:
        """本人情報抽出"""
        
    @staticmethod
    def extract_family_info(workbook) -> list[dict]:
        """家族情報抽出"""
```

**2. DateConverter**
```python
class DateConverter:
    """日付変換専用クラス"""
    
    @staticmethod
    def convert_wareki_to_seireki(date_str: str) -> str:
        """元号→西暦変換"""
        
    @staticmethod
    def calculate_age(birth_date: str) -> int:
        """年齢計算"""
        
    @staticmethod
    def normalize_date(date_str: str) -> str:
        """日付正規化"""
```

**3. NodeGenerator**
```python
class NodeGenerator:
    """ノード生成専用クラス"""
    
    def generate_person_node(self, data: dict) -> dict:
        """本人ノード生成"""
        
    def generate_family_node(self, data: dict) -> dict:
        """家族ノード生成"""
        
    def generate_notebook_node(self, data: dict) -> dict:
        """手帳ノード生成"""
```

**4. RelationGenerator**
```python
class RelationGenerator:
    """リレーション生成専用クラス"""
    
    def generate_family_relation(self, person_id: str, family_id: str, relation_type: str) -> dict:
        """家族関係生成"""
        
    def generate_contract_relation(self, person_id: str, contract_id: str) -> dict:
        """契約関係生成"""
```

**5. Validator**
```python
class Validator:
    """データ検証専用クラス"""
    
    @staticmethod
    def validate_required_fields(data: dict, required: list[str]) -> list[str]:
        """必須フィールド検証"""
        
    @staticmethod
    def validate_date_format(date_str: str) -> bool:
        """日付形式検証"""
        
    @staticmethod
    def validate_enum_value(value: str, allowed: list[str]) -> bool:
        """列挙型値検証"""
```

**6. HTMLGenerator**
```python
class HTMLGenerator:
    """HTML生成専用クラス"""
    
    def __init__(self, visualization_lib: str = "d3"):
        """初期化（d3 or cytoscape）"""
        
    def generate(self, json_data: dict, person_name: str) -> str:
        """HTML生成"""
        
    def _generate_header(self) -> str:
        """ヘッダー生成"""
        
    def _generate_visualization_script(self, json_data: dict) -> str:
        """可視化スクリプト生成"""
        
    def _generate_layer_control(self) -> str:
        """レイヤー制御UI生成"""
```

---

## データモデル

### JSONスキーマ構造

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["person", "nodes", "relations", "metadata"],
  "properties": {
    "person": {
      "type": "object",
      "description": "本人の基本情報"
    },
    "nodes": {
      "type": "array",
      "description": "ノードの配列"
    },
    "relations": {
      "type": "array",
      "description": "リレーションの配列"
    },
    "metadata": {
      "type": "object",
      "description": "メタデータ"
    }
  }
}
```

### ノードモデル

```python
class Node(TypedDict):
    """ノードの型定義"""
    id: str                    # UUID v4
    type: str                  # ノードタイプ（18種類）
    name: str                  # ノード名
    properties: dict           # ノード固有のプロパティ
    display: dict              # 表示設定
    layer: str                 # レイヤー名
    is_default_visible: bool   # デフォルト表示フラグ
    created_at: str            # 作成日時（ISO 8601）
```

**displayプロパティの詳細**:
```python
display = {
    "color": str,      # 色（例: "orange", "#FF6B35"）
    "size": str,       # サイズ（例: "large", "medium", "small"）
    "shape": str,      # 形状（現在は全て "circle"）
    "label": str,      # 表示ラベル
    "icon": str        # アイコン（オプション）
}
```

### リレーションモデル

```python
class Relation(TypedDict):
    """リレーションの型定義"""
    id: str                    # UUID v4
    type: str                  # リレーションタイプ（19種類）
    source_id: str             # 始点ノードID
    target_id: str             # 終点ノードID
    properties: dict           # リレーション固有のプロパティ
    direction: str             # 方向（"directed" or "undirected"）
    display: dict              # 表示設定
    layer: str                 # レイヤー名
    created_at: str            # 作成日時（ISO 8601）
```

**displayプロパティの詳細**:
```python
display = {
    "line_style": str,     # 線のスタイル（例: "solid", "dashed"）
    "line_width": int,     # 線の幅（ピクセル）
    "color": str,          # 色
    "arrow": bool,         # 矢印の有無
    "label": str           # 表示ラベル（オプション）
}
```

### メタデータモデル

```python
class Metadata(TypedDict):
    """メタデータの型定義"""
    created_at: str            # 作成日時（ISO 8601）
    created_by: str            # 作成者（システム名）
    version: str               # バージョン番号
    schema_version: str        # スキーマバージョン
    source_file: str           # 元ファイル名
    node_count: int            # ノード数
    relation_count: int        # リレーション数
    person_name: str           # 本人氏名
    person_age: int            # 本人年齢
```

---

## 処理フロー

### 1. Excel読み込みフロー

```python
def _load_excel(self) -> dict:
    """
    Excelファイルを読み込み、辞書形式で返す
    
    Returns:
        dict: {
            "person": {...},
            "family": [...],
            "notebooks": [...],
            "support_levels": [...],
            "diagnoses": [...],
            "legal_guardians": [...],
            "consultation_supports": [...],
            "service_plans": [...],
            "service_contracts": [...],
            "medical_institutions": [...]
        }
    """
    # 1. Excelファイルを開く
    workbook = openpyxl.load_workbook(self.input_file)
    
    # 2. 各シートからデータ抽出
    data = {
        "person": self._read_person_sheet(workbook),
        "family": self._read_family_sheet(workbook),
        "notebooks": self._read_notebooks_sheet(workbook),
        # ... 他のシート
    }
    
    # 3. ワークブックを閉じる
    workbook.close()
    
    return data
```

### 2. データ検証フロー

```python
def _validate_data(self, data: dict) -> list[str]:
    """
    データの整合性を検証
    
    Args:
        data: 読み込んだデータ
        
    Returns:
        list[str]: エラーメッセージのリスト（空ならエラーなし）
    """
    errors = []
    
    # 1. 必須フィールドチェック
    if not data["person"].get("name"):
        errors.append("本人の氏名が入力されていません")
    
    if not data["person"].get("birth_date"):
        errors.append("本人の生年月日が入力されていません")
    
    # 2. 日付形式チェック
    for notebook in data["notebooks"]:
        if not self._is_valid_date(notebook.get("issue_date")):
            errors.append(f"手帳の交付日が不正です: {notebook.get('issue_date')}")
    
    # 3. 列挙型値チェック
    for family in data["family"]:
        if family.get("living_together") not in ["○", "×", "Yes", "No"]:
            errors.append(f"家族の同居フラグが不正です: {family.get('living_together')}")
    
    return errors
```

### 3. 日付変換フロー

```python
def _convert_dates(self, data: dict) -> dict:
    """
    元号を西暦に変換し、年齢を計算
    
    Args:
        data: 読み込んだデータ
        
    Returns:
        dict: 変換後のデータ
    """
    converter = DateConverter()
    
    # 1. 本人の生年月日を変換
    birth_date_str = data["person"]["birth_date"]
    data["person"]["birth_date"] = converter.normalize_date(birth_date_str)
    data["person"]["age"] = converter.calculate_age(data["person"]["birth_date"])
    
    # 2. 家族の生年月日を変換
    for family in data["family"]:
        if family.get("birth_date"):
            family["birth_date"] = converter.normalize_date(family["birth_date"])
            family["age"] = converter.calculate_age(family["birth_date"])
    
    # 3. 各種日付を変換
    for notebook in data["notebooks"]:
        notebook["issue_date"] = converter.normalize_date(notebook["issue_date"])
        if notebook.get("expiry_date"):
            notebook["expiry_date"] = converter.normalize_date(notebook["expiry_date"])
    
    return data
```

### 4. ノード生成フロー

```python
def _generate_nodes(self, data: dict) -> list[dict]:
    """
    データからノードを生成
    
    Args:
        data: 変換後のデータ
        
    Returns:
        list[dict]: ノードのリスト
    """
    generator = NodeGenerator()
    nodes = []
    
    # 1. 本人ノード生成（必須）
    person_node = generator.generate_person_node(data["person"])
    nodes.append(person_node)
    
    # 2. 家族ノード生成
    for family_data in data["family"]:
        family_node = generator.generate_family_node(family_data)
        nodes.append(family_node)
    
    # 3. 手帳ノード生成
    for notebook_data in data["notebooks"]:
        notebook_node = generator.generate_notebook_node(notebook_data)
        nodes.append(notebook_node)
    
    # 4. その他のノード生成
    # ... 支援区分、診断、成年後見、サービスなど
    
    return nodes
```

### 5. リレーション生成フロー

```python
def _generate_relations(self, nodes: list[dict]) -> list[dict]:
    """
    ノード間のリレーションを生成
    
    Args:
        nodes: ノードのリスト
        
    Returns:
        list[dict]: リレーションのリスト
    """
    generator = RelationGenerator()
    relations = []
    
    # 1. 本人ノードを取得
    person_node = next(n for n in nodes if n["type"] == "Person")
    
    # 2. 家族リレーション生成
    family_nodes = [n for n in nodes if n["type"] == "Family"]
    for family_node in family_nodes:
        relation = generator.generate_family_relation(
            person_node["id"],
            family_node["id"],
            family_node["properties"]["relation_type"]
        )
        relations.append(relation)
    
    # 3. 手帳リレーション生成
    notebook_nodes = [n for n in nodes if "Notebook" in n["type"]]
    for notebook_node in notebook_nodes:
        relation = generator.generate_notebook_relation(
            person_node["id"],
            notebook_node["id"]
        )
        relations.append(relation)
    
    # 4. その他のリレーション生成
    # ...
    
    return relations
```

---

## 可視化エンジン

### D3.jsによる実装例

```javascript
// グラフデータの準備
const graphData = {
    nodes: jsonData.nodes.map(n => ({
        id: n.id,
        name: n.name,
        type: n.type,
        color: n.display.color,
        size: n.display.size === "large" ? 50 : n.display.size === "medium" ? 30 : 20,
        layer: n.layer,
        visible: n.is_default_visible
    })),
    links: jsonData.relations.map(r => ({
        source: r.source_id,
        target: r.target_id,
        type: r.type,
        directed: r.direction === "directed"
    }))
};

// D3.js force simulationの設定
const simulation = d3.forceSimulation(graphData.nodes)
    .force("link", d3.forceLink(graphData.links).id(d => d.id).distance(100))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide().radius(d => d.size + 10));

// SVG要素の作成
const svg = d3.select("#ecomap")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

// リンクの描画
const link = svg.append("g")
    .selectAll("line")
    .data(graphData.links)
    .enter().append("line")
    .attr("stroke", "#999")
    .attr("stroke-width", 2);

// ノードの描画
const node = svg.append("g")
    .selectAll("circle")
    .data(graphData.nodes)
    .enter().append("circle")
    .attr("r", d => d.size)
    .attr("fill", d => d.color)
    .call(drag(simulation));

// ラベルの描画
const label = svg.append("g")
    .selectAll("text")
    .data(graphData.nodes)
    .enter().append("text")
    .text(d => d.name)
    .attr("font-size", 12)
    .attr("dx", 15)
    .attr("dy", 4);

// シミュレーションの更新
simulation.on("tick", () => {
    link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);
    
    node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
    
    label
        .attr("x", d => d.x)
        .attr("y", d => d.y);
});
```

### Cytoscape.jsによる実装例

```javascript
// Cytoscape.jsの初期化
const cy = cytoscape({
    container: document.getElementById('ecomap'),
    
    elements: [
        // ノード
        ...jsonData.nodes.map(n => ({
            data: {
                id: n.id,
                label: n.name,
                type: n.type,
                layer: n.layer
            },
            style: {
                'background-color': n.display.color,
                'width': n.display.size === 'large' ? 50 : 30,
                'height': n.display.size === 'large' ? 50 : 30
            }
        })),
        
        // エッジ
        ...jsonData.relations.map(r => ({
            data: {
                source: r.source_id,
                target: r.target_id,
                label: r.type
            }
        }))
    ],
    
    style: [
        {
            selector: 'node',
            style: {
                'label': 'data(label)',
                'text-valign': 'center',
                'text-halign': 'right',
                'font-size': '12px'
            }
        },
        {
            selector: 'edge',
            style: {
                'width': 2,
                'line-color': '#999',
                'target-arrow-color': '#999',
                'target-arrow-shape': 'triangle'
            }
        }
    ],
    
    layout: {
        name: 'cose',  // Force-directed layout
        animate: true,
        nodeRepulsion: 8000,
        idealEdgeLength: 100
    }
});

// イベントハンドラー
cy.on('tap', 'node', function(evt){
    const node = evt.target;
    showNodeDetails(node.data());
});
```

### レイヤー制御の実装

```javascript
// レイヤー切り替え関数
function toggleLayer(layerName, visible) {
    // ノードの表示/非表示
    cy.nodes().forEach(node => {
        if (node.data('layer') === layerName) {
            if (visible) {
                node.style('display', 'element');
            } else {
                node.style('display', 'none');
            }
        }
    });
    
    // エッジの表示/非表示
    cy.edges().forEach(edge => {
        const sourceLayer = edge.source().data('layer');
        const targetLayer = edge.target().data('layer');
        
        if (sourceLayer === layerName || targetLayer === layerName) {
            if (visible && 
                edge.source().style('display') !== 'none' &&
                edge.target().style('display') !== 'none') {
                edge.style('display', 'element');
            } else {
                edge.style('display', 'none');
            }
        }
    });
}

// UIイベント
document.getElementById('layer-family').addEventListener('change', function(e) {
    toggleLayer('family', e.target.checked);
});

document.getElementById('layer-medical').addEventListener('change', function(e) {
    toggleLayer('medical', e.target.checked);
});
```

---

## パフォーマンス要件

### 処理時間目標

| 処理 | 目標時間 | 最大許容時間 |
|------|---------|-------------|
| Excel読み込み | < 1秒 | 3秒 |
| データ変換 | < 0.5秒 | 1秒 |
| ノード生成 | < 1秒 | 2秒 |
| JSON出力 | < 0.5秒 | 1秒 |
| HTML生成 | < 1秒 | 2秒 |
| **合計** | **< 4秒** | **9秒** |

### メモリ使用量

| データ規模 | 推奨メモリ | 最大メモリ |
|-----------|-----------|-----------|
| 小規模（~20ノード） | 50MB | 100MB |
| 中規模（~50ノード） | 100MB | 200MB |
| 大規模（~100ノード） | 200MB | 400MB |

### ファイルサイズ

| ファイル | 推奨サイズ | 最大サイズ |
|---------|----------|-----------|
| JSONファイル | < 100KB | 500KB |
| HTMLファイル | < 500KB | 1MB |

### 最適化戦略

1. **遅延読み込み**: シートごとに順次読み込み
2. **キャッシング**: 変換済みデータのキャッシュ
3. **並列処理**: 可能な部分は並列化（将来的な拡張）
4. **ストリーミング**: 大規模データの場合はストリーミング処理

---

## セキュリティ

### データ保護

1. **ローカル処理**: 全ての処理はローカル環境で実行
2. **外部通信なし**: インターネット経由のデータ送信なし
3. **ファイル権限**: 生成ファイルの適切な権限設定

### 入力検証

1. **ファイル形式チェック**: 許可された形式のみ処理
2. **データサイズ制限**: 異常に大きいデータの拒否
3. **SQLインジェクション対策**: 不要（データベース不使用）
4. **XSS対策**: HTML生成時のエスケープ処理

### エラーハンドリング

```python
try:
    # 処理
    result = process_data(input_file)
except FileNotFoundError:
    logger.error(f"ファイルが見つかりません: {input_file}")
    raise
except ValidationError as e:
    logger.error(f"データ検証エラー: {e}")
    raise
except Exception as e:
    logger.error(f"予期しないエラー: {e}", exc_info=True)
    raise
finally:
    # クリーンアップ処理
    cleanup()
```

---

## 拡張性

### 新しいノードタイプの追加

1. `schema.json` にノードタイプ定義を追加
2. `NodeGenerator` クラスに生成メソッドを追加
3. `ExcelReader` クラスにシート読み込みメソッドを追加
4. テンプレートに新しいシートを追加

### 新しいリレーションタイプの追加

1. `schema.json` にリレーションタイプ定義を追加
2. `RelationGenerator` クラスに生成メソッドを追加
3. ドキュメントを更新

### CSV形式のサポート

```python
class CSVReader:
    """CSV読み込みクラス"""
    
    @staticmethod
    def read_csv(file_path: str) -> list[dict]:
        """CSVファイルを読み込み"""
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
```

### データベース連携（将来的な拡張）

```python
class DatabaseConnector:
    """データベース接続クラス（将来的な拡張）"""
    
    def __init__(self, db_path: str):
        """初期化"""
        
    def save_ecomap(self, json_data: dict) -> int:
        """エコマップをデータベースに保存"""
        
    def load_ecomap(self, ecomap_id: int) -> dict:
        """エコマップをデータベースから読み込み"""
```

---

## 付録

### ディレクトリ構造（詳細版）

```
~/AI-Workspace/ecomap-creator/
├── ecomap_creator.py          # メインスクリプト
├── modules/                   # モジュールディレクトリ
│   ├── __init__.py
│   ├── excel_reader.py       # Excel読み込み
│   ├── date_converter.py     # 日付変換
│   ├── node_generator.py     # ノード生成
│   ├── relation_generator.py # リレーション生成
│   ├── validator.py          # データ検証
│   └── html_generator.py     # HTML生成
├── templates/                 # テンプレート
│   ├── template.xlsx
│   └── html_template.html    # HTML生成用テンプレート
├── samples/                   # サンプルデータ
│   ├── sample_case_01.xlsx
│   ├── sample_case_01.json
│   ├── sample_case_02.xlsx
│   ├── sample_case_02.json
│   ├── sample_case_03.xlsx
│   └── sample_case_03.json
├── outputs/                   # 出力ファイル
│   └── (生成されたファイル)
├── tests/                     # テストコード
│   ├── __init__.py
│   ├── test_excel_reader.py
│   ├── test_date_converter.py
│   ├── test_node_generator.py
│   └── test_validator.py
├── docs/                      # ドキュメント
│   ├── SKILL.md
│   ├── TECHNICAL_SPEC.md     # このファイル
│   ├── API_SPEC.md
│   ├── USAGE_GUIDE.md
│   └── DATA_CONVERSION_RULES.md
├── schema.json               # JSONスキーマ
├── requirements.txt          # 依存ライブラリ
├── setup.py                  # セットアップスクリプト
├── .gitignore               # Git無視ファイル
└── README.md                 # プロジェクト概要
```

### 依存ライブラリ（requirements.txt）

```
openpyxl>=3.1.5
jsonschema>=4.0.0
```

### セットアップスクリプト（setup.py）

```python
from setuptools import setup, find_packages

setup(
    name='ecomap-creator',
    version='1.0.0',
    description='エコマップ作成スキル',
    author='K. Kawahara',
    packages=find_packages(),
    install_requires=[
        'openpyxl>=3.1.5',
    ],
    entry_points={
        'console_scripts': [
            'ecomap=ecomap_creator:main',
        ],
    },
)
```

---

**以上、エコマップ作成スキルの技術仕様書でした。**
