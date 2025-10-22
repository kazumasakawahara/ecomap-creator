# 🎯 Phase 2 実行手順

## ✅ Phase 2 で作成したもの

Phase 2では、以下の3つのファイルを作成しました：

1. **template_creator.py** - Excelテンプレートを生成するPythonスクリプト
2. **sample_data_creator.py** - サンプルデータ3パターンを生成するPythonスクリプト
3. **USAGE_GUIDE.md** - テンプレートの記入ガイド（使い方説明書）

---

## 📝 Excelファイルを生成する手順

以下の手順で、Excelテンプレートとサンプルデータを生成してください。

### 準備: openpyxlのインストール確認

まず、必要なPythonライブラリがインストールされているか確認します。

```bash
python3 -c "import openpyxl; print(f'✅ openpyxl バージョン: {openpyxl.__version__}')" || echo "❌ openpyxlがインストールされていません"
```

もしインストールされていない場合は、以下のコマンドでインストールしてください：

```bash
pip3 install openpyxl
```

---

### ステップ1: テンプレートファイルの生成

エコマップ作成用のディレクトリに移動し、テンプレート作成スクリプトを実行します。

```bash
cd ~/AI-Workspace/ecomap-creator
python3 template_creator.py
```

**実行結果**:
```
📝 エコマップExcelテンプレートを作成中...
  → 1. 本人情報シート作成中...
  → 2. 家族情報シート作成中...
  （中略）
  → 10. 医療機関情報シート作成中...

✅ テンプレート作成完了！
📁 保存先: templates/template.xlsx
📊 シート数: 10枚
```

**生成されるファイル**:
- `templates/template.xlsx` - 空の入力用テンプレート（10シート）

---

### ステップ2: サンプルデータの生成

続いて、サンプルデータ作成スクリプトを実行します。

```bash
python3 sample_data_creator.py
```

**実行結果**:
```
📝 エコマップサンプルデータを作成中...

  → ケース1: 若年層・家族同居（佐藤健太さん）
     ✅ 保存完了: samples/sample_case_01.xlsx

  → ケース2: 中年層・グループホーム（田中花子さん）
     ✅ 保存完了: samples/sample_case_02.xlsx

  → ケース3: 高齢層・成年後見あり（鈴木正雄さん）
     ✅ 保存完了: samples/sample_case_03.xlsx

🎉 サンプルデータ作成完了！
```

**生成されるファイル**:
- `samples/sample_case_01.xlsx` - ケース1: 若年層・家族同居（佐藤健太さん）
- `samples/sample_case_02.xlsx` - ケース2: 中年層・グループホーム（田中花子さん）
- `samples/sample_case_03.xlsx` - ケース3: 高齢層・成年後見あり（鈴木正雄さん）

---

## 📁 生成されたファイルの確認

すべてのファイルが正常に作成されたか確認します。

```bash
ls -lh templates/
ls -lh samples/
```

**期待される出力**:
```
templates/
  template.xlsx  (約14KB)

samples/
  sample_case_01.xlsx  (約15-20KB)
  sample_case_02.xlsx  (約15-20KB)
  sample_case_03.xlsx  (約15-20KB)
```

---

## 🎯 次のステップ

Excelファイルの生成が完了したら、以下を確認してください：

### 1. テンプレートファイルの確認

Excelで `templates/template.xlsx` を開き、以下を確認してください：

- ✅ 10枚のシートがある
- ✅ 各シートにヘッダー行がある
- ✅ ヘッダー行が青色で表示されている
- ✅ 例示データ（「例：」で始まる行）がある

### 2. サンプルデータファイルの確認

Excelで `samples/sample_case_01.xlsx` を開き、以下を確認してください：

- ✅ 本人情報シートに「佐藤健太」さんの情報が入力されている
- ✅ 家族情報シートに家族メンバーが入力されている
- ✅ 各シートにデータが適切に入力されている

---

## ⚠️ トラブルシューティング

### エラー: `ModuleNotFoundError: No module named 'openpyxl'`

**原因**: openpyxlライブラリがインストールされていません。

**解決方法**:
```bash
pip3 install openpyxl
```

---

### エラー: `FileNotFoundError: [Errno 2] No such file or directory: 'templates/'`

**原因**: templatesディレクトリが存在しません。

**解決方法**:
```bash
mkdir -p templates samples
```

その後、再度スクリプトを実行してください。

---

### エラー: `Permission denied`

**原因**: ファイルの書き込み権限がありません。

**解決方法**:
```bash
chmod +w templates/ samples/
```

---

## 📚 参考資料

- **USAGE_GUIDE.md** - テンプレートの詳しい記入方法
- **ECOMAP_HANDOVER.md** - プロジェクト全体の引き継ぎ情報

---

## 🎉 Phase 2 完了！

Excelファイルの生成が完了したら、**Phase 3: スキーマ確定**に進む準備が整います。

次回は以下の作業を行います：
1. JSONスキーマ完全版の作成
2. データ変換ルールの定義（元号→西暦変換）
3. エコマップ可視化のためのデータ構造設計

---

**※このファイルは、Phase 2の作業記録として保存されています。**
