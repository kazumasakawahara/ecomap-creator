#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
日付変換モジュール

元号から西暦への変換、年齢計算、日付正規化などの機能を提供します。
"""

import re
from datetime import datetime, date
from typing import Optional


class DateConverter:
    """日付変換クラス"""
    
    # 元号変換テーブル
    WAREKI_TABLE = {
        "令和": 2018,
        "平成": 1988,
        "昭和": 1925,
        "大正": 1911,
        "明治": 1867,
    }
    
    @staticmethod
    def convert_wareki_to_seireki(date_str: str) -> str:
        """
        元号を西暦に変換
        
        Args:
            date_str: 元号形式の日付（例: "令和5年4月1日"）
            
        Returns:
            西暦形式の日付（YYYY-MM-DD）
            
        Examples:
            >>> DateConverter.convert_wareki_to_seireki("令和5年4月1日")
            '2023-04-01'
            >>> DateConverter.convert_wareki_to_seireki("平成25年12月31日")
            '2013-12-31'
        """
        if not date_str:
            return ""
        
        # 元号パターン: 令和5年4月1日 or 令和5-04-01
        pattern = r"(令和|平成|昭和|大正|明治)(\d+)年?[\s\-/]*(\d+)月?[\s\-/]*(\d+)日?"
        match = re.search(pattern, date_str)
        
        if match:
            era = match.group(1)
            year = int(match.group(2))
            month = int(match.group(3))
            day = int(match.group(4))
            
            # 西暦に変換
            seireki_year = DateConverter.WAREKI_TABLE[era] + year
            
            # YYYY-MM-DD形式で返す
            return f"{seireki_year:04d}-{month:02d}-{day:02d}"
        
        # 元号パターンにマッチしない場合は元の文字列を返す
        return date_str
    
    @staticmethod
    def calculate_age(birth_date: str, reference_date: Optional[str] = None) -> int:
        """
        年齢を計算
        
        Args:
            birth_date: 生年月日（YYYY-MM-DD）
            reference_date: 基準日（省略時は今日）
            
        Returns:
            年齢
            
        Examples:
            >>> DateConverter.calculate_age("2021-04-15")  # 今日が2025-10-21の場合
            4
            >>> DateConverter.calculate_age("1955-03-15")
            70
        """
        if not birth_date:
            return 0
        
        try:
            # 生年月日をパース
            birth = datetime.strptime(birth_date, "%Y-%m-%d").date()
            
            # 基準日を設定
            if reference_date:
                ref = datetime.strptime(reference_date, "%Y-%m-%d").date()
            else:
                ref = date.today()
            
            # 年齢を計算
            age = ref.year - birth.year
            
            # 誕生日がまだ来ていない場合は1歳引く
            if (ref.month, ref.day) < (birth.month, birth.day):
                age -= 1
            
            return age
            
        except (ValueError, TypeError):
            return 0
    
    @staticmethod
    def normalize_date(date_str: str) -> str:
        """
        日付を正規化（YYYY-MM-DD形式に統一）
        
        Args:
            date_str: 日付文字列（様々な形式）
            
        Returns:
            正規化された日付（YYYY-MM-DD）
            
        Examples:
            >>> DateConverter.normalize_date("令和5年4月1日")
            '2023-04-01'
            >>> DateConverter.normalize_date("2023/4/1")
            '2023-04-01'
            >>> DateConverter.normalize_date("2023年4月1日")
            '2023-04-01'
        """
        if not date_str:
            return ""
        
        # すでに正規化されている場合
        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            return date_str
        
        # 元号形式の場合
        if any(era in date_str for era in DateConverter.WAREKI_TABLE.keys()):
            return DateConverter.convert_wareki_to_seireki(date_str)
        
        # スラッシュ区切り: 2023/4/1 → 2023-04-01
        slash_pattern = r"(\d{4})\s*/\s*(\d{1,2})\s*/\s*(\d{1,2})"
        match = re.search(slash_pattern, date_str)
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            return f"{year:04d}-{month:02d}-{day:02d}"
        
        # 年月日形式: 2023年4月1日 → 2023-04-01
        year_pattern = r"(\d{4})年\s*(\d{1,2})月\s*(\d{1,2})日?"
        match = re.search(year_pattern, date_str)
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            return f"{year:04d}-{month:02d}-{day:02d}"
        
        # ハイフン区切り（ゼロパディングなし）: 2023-4-1 → 2023-04-01
        hyphen_pattern = r"(\d{4})\s*-\s*(\d{1,2})\s*-\s*(\d{1,2})"
        match = re.search(hyphen_pattern, date_str)
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            return f"{year:04d}-{month:02d}-{day:02d}"
        
        # パースできない場合は空文字列を返す
        return ""
    
    @staticmethod
    def is_valid_date(date_str: str) -> bool:
        """
        日付が有効かどうかを確認
        
        Args:
            date_str: 日付文字列
            
        Returns:
            有効な日付ならTrue
        """
        if not date_str:
            return False
        
        try:
            # 正規化を試みる
            normalized = DateConverter.normalize_date(date_str)
            if not normalized:
                return False
            
            # 実際に日付として解釈できるか確認
            datetime.strptime(normalized, "%Y-%m-%d")
            return True
            
        except (ValueError, TypeError):
            return False


if __name__ == "__main__":
    # テスト
    print("=== DateConverter テスト ===")
    
    # 元号→西暦変換
    print("\n【元号→西暦変換】")
    test_dates = [
        "令和5年4月1日",
        "平成25年12月31日",
        "昭和60年3月15日",
    ]
    for d in test_dates:
        print(f"{d} → {DateConverter.convert_wareki_to_seireki(d)}")
    
    # 年齢計算
    print("\n【年齢計算】")
    test_births = [
        "2021-04-15",
        "1955-03-15",
        "1990-08-25",
    ]
    for b in test_births:
        age = DateConverter.calculate_age(b)
        print(f"{b} → {age}歳")
    
    # 日付正規化
    print("\n【日付正規化】")
    test_formats = [
        "令和5年4月1日",
        "2023/4/1",
        "2023年4月1日",
        "2023-4-1",
    ]
    for f in test_formats:
        print(f"{f} → {DateConverter.normalize_date(f)}")
    
    # 日付検証
    print("\n【日付検証】")
    test_validates = [
        "2023-04-01",
        "令和5年4月1日",
        "invalid",
        "2023/4/1",
    ]
    for v in test_validates:
        valid = DateConverter.is_valid_date(v)
        print(f"{v} → {'有効' if valid else '無効'}")
