#!/bin/bash
# Claude Skill パッケージング自動化スクリプト
# ecomap-creatorをClaude Desktop用にZIPパッケージ化します

set -e  # エラーで停止

# 色付きログ関数
log_info() { echo -e "\033[0;32m[INFO]\033[0m $1"; }
log_warn() { echo -e "\033[0;33m[WARN]\033[0m $1"; }
log_error() { echo -e "\033[0;31m[ERROR]\033[0m $1"; }

# バージョン取得（pyproject.tomlから）
VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
if [ -z "$VERSION" ]; then
    log_error "バージョン番号を取得できませんでした"
    exit 1
fi

log_info "ecomap-creator v$VERSION のパッケージングを開始します"

# 出力ファイル名
PACKAGE_NAME="ecomap-creator-v${VERSION}.zip"
BUILD_DIR="build_package"

# クリーンアップ
log_info "既存のビルドディレクトリをクリーンアップ中..."
rm -rf "$BUILD_DIR"
rm -f "$PACKAGE_NAME"

# ビルドディレクトリ作成
log_info "ビルドディレクトリを作成中..."
mkdir -p "$BUILD_DIR/ecomap-creator"

# 必要なファイルをコピー
log_info "必要なファイルをコピー中..."

# Pythonファイル
cp ecomap_creator.py "$BUILD_DIR/ecomap-creator/"

# モジュールディレクトリ
cp -r modules "$BUILD_DIR/ecomap-creator/"

# テンプレートとサンプル
cp -r templates "$BUILD_DIR/ecomap-creator/"
cp -r samples "$BUILD_DIR/ecomap-creator/"

# 設定ファイル
cp schema.json "$BUILD_DIR/ecomap-creator/"
cp pyproject.toml "$BUILD_DIR/ecomap-creator/"

# ドキュメント
cp SKILL.md "$BUILD_DIR/ecomap-creator/"
cp README.md "$BUILD_DIR/ecomap-creator/"
cp DATA_CONVERSION_RULES.md "$BUILD_DIR/ecomap-creator/"
cp USAGE_GUIDE.md "$BUILD_DIR/ecomap-creator/"

# Pythonキャッシュとuvファイルを除外してクリーンアップ
log_info "不要なファイルを削除中..."
find "$BUILD_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$BUILD_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true
find "$BUILD_DIR" -type f -name ".DS_Store" -delete 2>/dev/null || true

# ZIPファイルを作成
log_info "ZIPファイルを作成中: $PACKAGE_NAME"
cd "$BUILD_DIR"
zip -r "../$PACKAGE_NAME" ecomap-creator -q
cd ..

# クリーンアップ
log_info "ビルドディレクトリをクリーンアップ中..."
rm -rf "$BUILD_DIR"

# 結果表示
if [ -f "$PACKAGE_NAME" ]; then
    FILE_SIZE=$(du -h "$PACKAGE_NAME" | cut -f1)
    log_info "✓ パッケージング完了！"
    echo ""
    echo "  パッケージ: $PACKAGE_NAME"
    echo "  サイズ: $FILE_SIZE"
    echo ""
    echo "📦 Claude Desktopへのアップロード手順:"
    echo "  1. Claude Desktopを開く"
    echo "  2. Settings → Skills → Upload Skill"
    echo "  3. $PACKAGE_NAME を選択してアップロード"
    echo ""
    echo "使用例:"
    echo '  「佐藤健太さんのエコマップを作成してください」'
    echo ""
else
    log_error "パッケージング失敗"
    exit 1
fi
