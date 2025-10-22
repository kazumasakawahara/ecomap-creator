#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
データ検証モジュール

入力データの検証を行います。
"""

from typing import List, Dict, Any, Optional
from .date_converter import DateConverter


class Validator:
    """データ検証クラス"""
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required: List[str]) -> List[str]:
        """
        必須フィールドを検証
        
        Args:
            data: 検証するデータ
            required: 必須フィールドのリスト
            
        Returns:
            エラーメッセージのリスト（空ならエラーなし）
            
        Examples:
            >>> data = {"name": "山田太郎", "age": 30}
            >>> required = ["name", "age", "address"]
            >>> Validator.validate_required_fields(data, required)
            ['addressが入力されていません']
        """
        errors = []
        
        for field in required:
            if field not in data or not data[field]:
                errors.append(f"{field}が入力されていません")
        
        return errors
    
    @staticmethod
    def validate_date_format(date_str: str) -> bool:
        """
        日付形式を検証
        
        Args:
            date_str: 日付文字列
            
        Returns:
            有効な形式ならTrue
            
        Examples:
            >>> Validator.validate_date_format("2023-04-01")
            True
            >>> Validator.validate_date_format("令和5年4月1日")
            True
            >>> Validator.validate_date_format("invalid")
            False
        """
        return DateConverter.is_valid_date(date_str)
    
    @staticmethod
    def validate_enum_value(value: str, allowed: List[str]) -> bool:
        """
        列挙型値を検証
        
        Args:
            value: 検証する値
            allowed: 許可された値のリスト
            
        Returns:
            許可された値ならTrue
            
        Examples:
            >>> Validator.validate_enum_value("男", ["男", "女", "その他"])
            True
            >>> Validator.validate_enum_value("不明", ["男", "女", "その他"])
            False
        """
        return value in allowed
    
    @staticmethod
    def validate_person_info(data: Dict[str, Any]) -> List[str]:
        """
        本人情報を検証
        
        Args:
            data: 本人情報データ
            
        Returns:
            エラーメッセージのリスト
        """
        errors = []
        
        # 必須フィールド
        required = ["name", "birth_date", "gender"]
        errors.extend(Validator.validate_required_fields(data, required))
        
        # 生年月日の形式チェック
        if data.get("birth_date"):
            if not Validator.validate_date_format(data["birth_date"]):
                errors.append(f"生年月日の形式が不正です: {data['birth_date']}")
        
        # 性別の値チェック
        if data.get("gender"):
            allowed_genders = ["男", "女", "その他"]
            if not Validator.validate_enum_value(data["gender"], allowed_genders):
                errors.append(f"性別の値が不正です: {data['gender']}")
        
        return errors
    
    @staticmethod
    def validate_family_info(data: Dict[str, Any]) -> List[str]:
        """
        家族情報を検証
        
        Args:
            data: 家族情報データ
            
        Returns:
            エラーメッセージのリスト
        """
        errors = []
        
        # 必須フィールド
        required = ["name", "relation", "living_together"]
        errors.extend(Validator.validate_required_fields(data, required))
        
        # 生年月日の形式チェック（任意項目）
        if data.get("birth_date"):
            if not Validator.validate_date_format(data["birth_date"]):
                errors.append(f"家族（{data.get('name', '不明')}）の生年月日の形式が不正です: {data['birth_date']}")
        
        # 同居の値チェック
        if data.get("living_together"):
            allowed_values = ["○", "×", "Yes", "No", "yes", "no"]
            if not Validator.validate_enum_value(data["living_together"], allowed_values):
                errors.append(f"家族（{data.get('name', '不明')}）の同居フラグが不正です: {data['living_together']}")
        
        return errors
    
    @staticmethod
    def validate_notebook_info(data: Dict[str, Any]) -> List[str]:
        """
        手帳情報を検証
        
        Args:
            data: 手帳情報データ
            
        Returns:
            エラーメッセージのリスト
        """
        errors = []
        
        # 必須フィールド
        required = ["type", "grade", "issue_date", "issuing_authority", "status"]
        errors.extend(Validator.validate_required_fields(data, required))
        
        # 手帳種別の値チェック
        if data.get("type"):
            allowed_types = ["療育手帳", "精神保健福祉手帳", "身体障害者手帳"]
            if not Validator.validate_enum_value(data["type"], allowed_types):
                errors.append(f"手帳種別の値が不正です: {data['type']}")
        
        # 交付日の形式チェック
        if data.get("issue_date"):
            if not Validator.validate_date_format(data["issue_date"]):
                errors.append(f"手帳の交付日の形式が不正です: {data['issue_date']}")
        
        # 有効期限の形式チェック（任意項目）
        if data.get("expiry_date"):
            if not Validator.validate_date_format(data["expiry_date"]):
                errors.append(f"手帳の有効期限の形式が不正です: {data['expiry_date']}")
        
        # 状態の値チェック
        if data.get("status"):
            allowed_statuses = ["有効", "期限切れ", "更新済み"]
            if not Validator.validate_enum_value(data["status"], allowed_statuses):
                errors.append(f"手帳の状態の値が不正です: {data['status']}")
        
        return errors
    
    @staticmethod
    def validate_support_level_info(data: Dict[str, Any]) -> List[str]:
        """
        支援区分情報を検証
        
        Args:
            data: 支援区分情報データ
            
        Returns:
            エラーメッセージのリスト
        """
        errors = []
        
        # 必須フィールド
        required = ["level", "decision_date", "deciding_authority", "status"]
        errors.extend(Validator.validate_required_fields(data, required))
        
        # 支援区分の値チェック
        if data.get("level") is not None:
            try:
                level = int(data["level"])
                if level < 0 or level > 6:
                    errors.append(f"支援区分の値が不正です（0-6の範囲）: {level}")
            except (ValueError, TypeError):
                errors.append(f"支援区分の値が不正です: {data['level']}")
        
        # 決定日の形式チェック
        if data.get("decision_date"):
            if not Validator.validate_date_format(data["decision_date"]):
                errors.append(f"支援区分の決定日の形式が不正です: {data['decision_date']}")
        
        # 有効期限の形式チェック（任意項目）
        if data.get("expiry_date"):
            if not Validator.validate_date_format(data["expiry_date"]):
                errors.append(f"支援区分の有効期限の形式が不正です: {data['expiry_date']}")
        
        # 状態の値チェック
        if data.get("status"):
            allowed_statuses = ["現在", "期限切れ"]
            if not Validator.validate_enum_value(data["status"], allowed_statuses):
                errors.append(f"支援区分の状態の値が不正です: {data['status']}")
        
        return errors
    
    @staticmethod
    def validate_all_data(data: Dict[str, Any]) -> List[str]:
        """
        全データを検証
        
        Args:
            data: 全データ
            
        Returns:
            エラーメッセージのリスト
        """
        all_errors = []
        
        # 本人情報を検証
        if "person" in data:
            errors = Validator.validate_person_info(data["person"])
            all_errors.extend(errors)
        else:
            all_errors.append("本人情報が見つかりません")
        
        # 家族情報を検証
        if "family" in data:
            for i, family in enumerate(data["family"]):
                errors = Validator.validate_family_info(family)
                if errors:
                    all_errors.append(f"家族情報 {i+1}件目:")
                    all_errors.extend([f"  {e}" for e in errors])
        
        # 手帳情報を検証
        if "notebooks" in data:
            for i, notebook in enumerate(data["notebooks"]):
                errors = Validator.validate_notebook_info(notebook)
                if errors:
                    all_errors.append(f"手帳情報 {i+1}件目:")
                    all_errors.extend([f"  {e}" for e in errors])
        
        # 支援区分情報を検証
        if "support_levels" in data:
            for i, level in enumerate(data["support_levels"]):
                errors = Validator.validate_support_level_info(level)
                if errors:
                    all_errors.append(f"支援区分情報 {i+1}件目:")
                    all_errors.extend([f"  {e}" for e in errors])
        
        return all_errors


if __name__ == "__main__":
    # テスト
    print("=== Validator テスト ===")
    
    # 本人情報のテスト
    print("\n【本人情報の検証】")
    person_valid = {
        "name": "山田太郎",
        "birth_date": "2000-01-01",
        "gender": "男"
    }
    errors = Validator.validate_person_info(person_valid)
    print(f"正常なデータ: {errors if errors else 'エラーなし'}")
    
    person_invalid = {
        "name": "山田太郎",
        "birth_date": "invalid",
        "gender": "不明"
    }
    errors = Validator.validate_person_info(person_invalid)
    print(f"不正なデータ: {errors}")
    
    # 家族情報のテスト
    print("\n【家族情報の検証】")
    family_valid = {
        "name": "山田花子",
        "relation": "母",
        "living_together": "○"
    }
    errors = Validator.validate_family_info(family_valid)
    print(f"正常なデータ: {errors if errors else 'エラーなし'}")
    
    # 手帳情報のテスト
    print("\n【手帳情報の検証】")
    notebook_valid = {
        "type": "療育手帳",
        "grade": "A1",
        "issue_date": "2020-04-01",
        "issuing_authority": "北九州市",
        "status": "有効"
    }
    errors = Validator.validate_notebook_info(notebook_valid)
    print(f"正常なデータ: {errors if errors else 'エラーなし'}")
    
    # 支援区分情報のテスト
    print("\n【支援区分情報の検証】")
    support_level_valid = {
        "level": 6,
        "decision_date": "2021-04-01",
        "deciding_authority": "北九州市",
        "status": "現在"
    }
    errors = Validator.validate_support_level_info(support_level_valid)
    print(f"正常なデータ: {errors if errors else 'エラーなし'}")
