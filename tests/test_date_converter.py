#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日付変換モジュールのテスト
"""

import pytest
import sys
from pathlib import Path

# パスを追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.date_converter import DateConverter


def test_normalize_date_iso_format():
    """ISO形式の日付変換"""
    converter = DateConverter()
    assert converter.normalize_date("2021-04-15") == "2021-04-15"


def test_normalize_date_japanese_format():
    """日本語形式の日付変換"""
    converter = DateConverter()
    assert converter.normalize_date("2021年4月15日") == "2021-04-15"


def test_normalize_date_slash_format():
    """スラッシュ形式の日付変換"""
    converter = DateConverter()
    assert converter.normalize_date("2021/04/15") == "2021-04-15"


def test_calculate_age():
    """年齢計算"""
    converter = DateConverter()
    age = converter.calculate_age("2000-04-15")
    assert isinstance(age, int)
    assert age >= 24  # 2025年時点で24歳以上


def test_normalize_date_invalid():
    """不正な日付"""
    converter = DateConverter()
    assert converter.normalize_date("invalid") == "invalid"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
