#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive Dialog Engine for Ecomap Creator

このモジュールは、対話型インターフェースを提供し、ユーザーとの質問応答形式で
エコマップデータを収集します。
"""

from typing import Dict, List, Optional, Any
from enum import Enum
import re
from datetime import datetime


class DialogState(Enum):
    """対話の状態を表す列挙型"""
    INITIAL = "initial"
    COLLECT_PERSON = "collect_person"
    COLLECT_FAMILY = "collect_family"
    COLLECT_NOTEBOOK = "collect_notebook"
    COLLECT_SUPPORT_LEVEL = "collect_support_level"
    COLLECT_DIAGNOSIS = "collect_diagnosis"
    COLLECT_LEGAL_GUARDIAN = "collect_legal_guardian"
    COLLECT_SERVICE = "collect_service"
    COLLECT_MEDICAL = "collect_medical"
    COMPLETE = "complete"


class InteractiveDialogEngine:
    """
    対話型データ収集エンジン

    ステートマシンパターンを使用して、段階的にエコマップデータを収集します。
    """

    def __init__(self):
        """初期化"""
        self.state = DialogState.INITIAL
        self.collected_data: Dict[str, Any] = {
            "person": {},
            "family": [],
            "notebooks": [],
            "support_levels": [],
            "diagnoses": [],
            "legal_guardians": [],
            "consultation_supports": [],
            "service_plans": [],
            "service_contracts": [],
            "medical_institutions": []
        }
        self.current_item: Dict[str, Any] = {}
        self.step_count = 0
        self.total_steps = 8

    def start_session(self, person_name: Optional[str] = None) -> str:
        """
        セッション開始

        Args:
            person_name: 本人の氏名（省略可能）

        Returns:
            str: 初期メッセージ
        """
        self.state = DialogState.COLLECT_PERSON
        self.step_count = 1

        if person_name:
            self.collected_data["person"]["name"] = person_name
            greeting = f"承知しました。{person_name}さんのエコマップを作成します。"
        else:
            greeting = "エコマップを作成します。"

        return f"""{greeting}
いくつか質問させてください。

📊 進捗: ステップ {self.step_count}/{self.total_steps}
まず、本人情報についてお聞きします。

{self._get_person_questions()}"""

    def _get_person_questions(self) -> str:
        """本人情報の質問を取得"""
        questions = []

        if "name" not in self.collected_data["person"]:
            questions.append("- お名前を教えてください")

        if "birth_date" not in self.collected_data["person"]:
            questions.append("- 生年月日を教えてください（例: 2021-04-15 または 令和3年4月15日）")

        if "gender" not in self.collected_data["person"]:
            questions.append("- 性別を教えてください（男/女/その他）")

        return "\n".join(questions)

    def process_input(self, user_input: str) -> str:
        """
        ユーザー入力を処理

        Args:
            user_input: ユーザーからの入力

        Returns:
            str: 応答メッセージ
        """
        if self.state == DialogState.COLLECT_PERSON:
            return self._process_person_input(user_input)
        elif self.state == DialogState.COLLECT_FAMILY:
            return self._process_family_input(user_input)
        elif self.state == DialogState.COLLECT_NOTEBOOK:
            return self._process_notebook_input(user_input)
        elif self.state == DialogState.COLLECT_SUPPORT_LEVEL:
            return self._process_support_level_input(user_input)
        elif self.state == DialogState.COLLECT_DIAGNOSIS:
            return self._process_diagnosis_input(user_input)
        elif self.state == DialogState.COLLECT_LEGAL_GUARDIAN:
            return self._process_legal_guardian_input(user_input)
        elif self.state == DialogState.COLLECT_SERVICE:
            return self._process_service_input(user_input)
        elif self.state == DialogState.COLLECT_MEDICAL:
            return self._process_medical_input(user_input)
        else:
            return "セッションが完了しました。"

    def _process_person_input(self, user_input: str) -> str:
        """本人情報の入力を処理"""
        person = self.collected_data["person"]

        # 氏名の収集
        if "name" not in person:
            person["name"] = user_input.strip()
            return f"ありがとうございます。{person['name']}さんですね。\n\n{self._get_person_questions()}"

        # 生年月日の収集
        if "birth_date" not in person:
            birth_date = self._parse_date(user_input)
            if birth_date:
                person["birth_date"] = birth_date
                age = self._calculate_age(birth_date)
                person["age"] = age
                return f"ありがとうございます。{person['name']}さんは{age}歳ですね。\n\n{self._get_person_questions()}"
            else:
                return "申し訳ございません。日付の形式が正しくありません。\n例: 2021-04-15 または 令和3年4月15日\n\n再度、生年月日を教えてください。"

        # 性別の収集
        if "gender" not in person:
            gender = user_input.strip()
            if gender in ["男", "女", "その他"]:
                person["gender"] = gender
                # 本人情報完了、次のステップへ
                self.state = DialogState.COLLECT_FAMILY
                self.step_count = 2
                return f"""ありがとうございます。本人情報を確認しました。

✓ 氏名: {person['name']}
✓ 生年月日: {person['birth_date']} ({person['age']}歳)
✓ 性別: {person['gender']}

📊 進捗: ステップ {self.step_count}/{self.total_steps}
次に、ご家族の情報をお聞きします。

ご家族はいらっしゃいますか？
- いる場合: ご家族の情報を教えてください
- いない場合: 「なし」または「スキップ」と入力してください"""
            else:
                return "性別は「男」「女」「その他」のいずれかで入力してください。"

        return "本人情報の収集中です。"

    def _process_family_input(self, user_input: str) -> str:
        """家族情報の入力を処理"""
        # スキップの判定
        if user_input.strip().lower() in ["なし", "スキップ", "skip", "いない"]:
            self.state = DialogState.COLLECT_NOTEBOOK
            self.step_count = 3
            return f"""承知しました。

📊 進捗: ステップ {self.step_count}/{self.total_steps}
次に、手帳情報についてお聞きします。

以下の手帳をお持ちですか？
- 療育手帳
- 精神保健福祉手帳
- 身体障害者手帳

お持ちの手帳について教えてください。
お持ちでない場合は「なし」と入力してください。"""

        # 家族情報の収集（簡略版）
        # 実際の実装では、より詳細な情報収集が必要
        family_member = {
            "name": user_input.strip(),
            "relation": "未設定",
            "living_together": "未設定"
        }
        self.collected_data["family"].append(family_member)

        return f"""ありがとうございます。{family_member['name']}さんを追加しました。

他にご家族はいらっしゃいますか？
- いる場合: お名前を教えてください
- いない場合: 「次へ」と入力してください"""

    def _process_notebook_input(self, user_input: str) -> str:
        """手帳情報の入力を処理"""
        # スキップ判定
        if user_input.strip().lower() in ["なし", "スキップ", "skip", "ない", "次へ"]:
            self.state = DialogState.COLLECT_SUPPORT_LEVEL
            self.step_count = 4
            return self._get_support_level_questions()

        # 新しい手帳の追加開始
        if not self.current_item:
            # 手帳種別を収集
            notebook_types = ["療育手帳", "精神保健福祉手帳", "身体障害者手帳"]
            user_type = user_input.strip()

            if user_type in notebook_types:
                self.current_item = {"type": user_type}
                return f"{user_type}ですね。\n\n等級を教えてください（例: A1、2級、1種など）"
            else:
                return f"手帳種別は以下から選択してください:\n- {', '.join(notebook_types)}\n\nまたは「なし」と入力してください。"

        # 等級を収集
        elif "grade" not in self.current_item:
            self.current_item["grade"] = user_input.strip()
            return "交付日を教えてください（例: 2020-04-01）"

        # 交付日を収集
        elif "issue_date" not in self.current_item:
            date = self._parse_date(user_input)
            if date:
                self.current_item["issue_date"] = date
                return "有効期限を教えてください（期限がない場合は「なし」）"
            else:
                return "日付の形式が正しくありません。\n例: 2020-04-01 または 令和2年4月1日\n\n再度、交付日を教えてください。"

        # 有効期限を収集
        elif "expiry_date" not in self.current_item:
            if user_input.strip().lower() in ["なし", "ない", "期限なし"]:
                self.current_item["expiry_date"] = None
            else:
                date = self._parse_date(user_input)
                if date:
                    self.current_item["expiry_date"] = date
                else:
                    return "日付の形式が正しくありません。\n例: 2025-03-31 または「なし」\n\n再度、有効期限を教えてください。"

            # 手帳情報を保存
            self.current_item["number"] = ""
            self.current_item["issuing_authority"] = ""
            self.current_item["notes"] = ""
            self.collected_data["notebooks"].append(self.current_item)
            self.current_item = {}

            return f"""ありがとうございます。手帳情報を追加しました。

他に手帳はありますか？
- ある場合: 手帳種別を教えてください（療育手帳/精神保健福祉手帳/身体障害者手帳）
- ない場合: 「次へ」と入力してください"""

    def _process_support_level_input(self, user_input: str) -> str:
        """支援区分の入力を処理"""
        # スキップ判定
        if user_input.strip().lower() in ["なし", "スキップ", "skip", "ない", "次へ"]:
            self.state = DialogState.COLLECT_DIAGNOSIS
            self.step_count = 5
            return self._get_diagnosis_questions()

        # 新しい支援区分の追加開始
        if not self.current_item:
            # 支援区分を収集
            support_levels = ["区分0", "区分1", "区分2", "区分3", "区分4", "区分5", "区分6"]
            user_level = user_input.strip()

            # 柔軟な入力を受け付ける
            if user_level in support_levels or user_level in ["0", "1", "2", "3", "4", "5", "6"]:
                if user_level.isdigit():
                    user_level = f"区分{user_level}"
                self.current_item = {"level": user_level}
                return f"{user_level}ですね。\n\n認定日を教えてください（例: 2023-04-01）"
            else:
                return f"支援区分は以下から選択してください:\n- {', '.join(support_levels)}\n\nまたは「なし」と入力してください。"

        # 認定日を収集
        elif "decision_date" not in self.current_item:
            date = self._parse_date(user_input)
            if date:
                self.current_item["decision_date"] = date
                return "有効期限を教えてください（例: 2026-03-31）"
            else:
                return "日付の形式が正しくありません。\n例: 2023-04-01 または 令和5年4月1日\n\n再度、認定日を教えてください。"

        # 有効期限を収集
        elif "expiry_date" not in self.current_item:
            date = self._parse_date(user_input)
            if date:
                self.current_item["expiry_date"] = date
                # 支援区分情報を保存
                self.current_item["authority"] = ""
                self.current_item["notes"] = ""
                self.collected_data["support_levels"].append(self.current_item)
                self.current_item = {}

                # 次のステップへ
                self.state = DialogState.COLLECT_DIAGNOSIS
                self.step_count = 5
                return f"""ありがとうございます。支援区分情報を追加しました。

{self._get_diagnosis_questions()}"""
            else:
                return "日付の形式が正しくありません。\n例: 2026-03-31 または 令和8年3月31日\n\n再度、有効期限を教えてください。"

        return "支援区分情報を収集中..."

    def _process_diagnosis_input(self, user_input: str) -> str:
        """診断情報の入力を処理"""
        # スキップ判定
        if user_input.strip().lower() in ["なし", "スキップ", "skip", "ない", "次へ"]:
            self.state = DialogState.COLLECT_LEGAL_GUARDIAN
            self.step_count = 6
            return self._get_legal_guardian_questions()

        # 新しい診断の追加開始
        if not self.current_item:
            # 診断名を収集
            self.current_item = {"name": user_input.strip()}
            return f"診断名「{user_input.strip()}」を登録します。\n\n診断日を教えてください（例: 2005-06-15、わからない場合は「不明」）"

        # 診断日を収集
        elif "diagnosis_date" not in self.current_item:
            if user_input.strip().lower() in ["不明", "わからない", "覚えていない"]:
                self.current_item["diagnosis_date"] = ""
            else:
                date = self._parse_date(user_input)
                if date:
                    self.current_item["diagnosis_date"] = date
                else:
                    return "日付の形式が正しくありません。\n例: 2005-06-15 または「不明」\n\n再度、診断日を教えてください。"

            # 診断情報を保存
            self.current_item["institution"] = ""
            self.current_item["doctor"] = ""
            self.current_item["icd_code"] = ""
            self.current_item["notes"] = ""
            self.collected_data["diagnoses"].append(self.current_item)
            self.current_item = {}

            return f"""ありがとうございます。診断情報を追加しました。

他に診断はありますか？
- ある場合: 診断名を教えてください
- ない場合: 「次へ」と入力してください"""

        return "診断情報を収集中..."

    def _process_legal_guardian_input(self, user_input: str) -> str:
        """成年後見の入力を処理"""
        # スキップ判定（成年後見は通常1つのみ）
        if user_input.strip().lower() in ["なし", "スキップ", "skip", "ない", "利用していない"]:
            self.state = DialogState.COLLECT_SERVICE
            self.step_count = 7
            return self._get_service_questions()

        # 成年後見制度を利用している場合
        if not self.current_item:
            # 簡略版: 利用しているという応答のみ
            self.current_item = {
                "guardian_name": "",
                "guardian_type": "成年後見人",
                "appointment_date": "",
                "relation": "",
                "contact": "",
                "notes": user_input.strip()
            }
            self.collected_data["legal_guardians"].append(self.current_item)
            self.current_item = {}

            # 次のステップへ
            self.state = DialogState.COLLECT_SERVICE
            self.step_count = 7
            return f"""承知しました。成年後見制度の利用を記録しました。

{self._get_service_questions()}"""

        return "成年後見情報を収集中..."

    def _process_service_input(self, user_input: str) -> str:
        """サービス情報の入力を処理"""
        # スキップ判定
        if user_input.strip().lower() in ["なし", "スキップ", "skip", "ない", "次へ", "利用していない"]:
            self.state = DialogState.COLLECT_MEDICAL
            self.step_count = 8
            return self._get_medical_questions()

        # 新しいサービスの追加開始
        if not self.current_item:
            # サービス種類を収集
            self.current_item = {"service_type": user_input.strip()}
            return f"サービス種類「{user_input.strip()}」を登録します。\n\n事業所名を教えてください"

        # 事業所名を収集
        elif "office_name" not in self.current_item:
            self.current_item["office_name"] = user_input.strip()
            self.current_item["office_number"] = ""
            self.current_item["contract_date"] = ""
            self.current_item["manager"] = ""
            self.current_item["usage_days"] = ""
            self.current_item["notes"] = ""

            # サービス契約情報を保存
            self.collected_data["service_contracts"].append(self.current_item)
            self.current_item = {}

            return f"""ありがとうございます。サービス情報を追加しました。

他に利用しているサービスはありますか？
- ある場合: サービス種類を教えてください（例: 生活介護、就労継続支援B型など）
- ない場合: 「次へ」と入力してください"""

        return "サービス情報を収集中..."

    def _process_medical_input(self, user_input: str) -> str:
        """医療情報の入力を処理"""
        # スキップ・完了判定
        if user_input.strip().lower() in ["なし", "スキップ", "skip", "ない", "完了", "通院していない"]:
            self.state = DialogState.COMPLETE
            return self._generate_summary()

        # 新しい医療機関の追加開始
        if not self.current_item:
            # 医療機関名を収集
            self.current_item = {"name": user_input.strip()}
            return f"医療機関「{user_input.strip()}」を登録します。\n\n診療科を教えてください（例: 精神科、内科など）"

        # 診療科を収集
        elif "department" not in self.current_item:
            self.current_item["department"] = user_input.strip()
            self.current_item["doctor"] = ""
            self.current_item["address"] = ""
            self.current_item["phone"] = ""
            self.current_item["start_date"] = ""
            self.current_item["medications"] = []
            self.current_item["notes"] = ""

            # 医療機関情報を保存
            self.collected_data["medical_institutions"].append(self.current_item)
            self.current_item = {}

            return f"""ありがとうございます。医療機関情報を追加しました。

他に通院している医療機関はありますか？
- ある場合: 医療機関名を教えてください
- ない場合: 「完了」と入力してください"""

        return "医療情報を収集中..."

    def _get_support_level_questions(self) -> str:
        """支援区分の質問を取得"""
        return f"""📊 進捗: ステップ {self.step_count}/{self.total_steps}
支援区分についてお聞きします。

障害支援区分をお持ちですか？（区分0〜6）
お持ちでない場合は「なし」と入力してください。"""

    def _get_diagnosis_questions(self) -> str:
        """診断情報の質問を取得"""
        return f"""📊 進捗: ステップ {self.step_count}/{self.total_steps}
診断情報についてお聞きします。

診断名を教えてください。
診断を受けていない場合は「なし」と入力してください。"""

    def _get_legal_guardian_questions(self) -> str:
        """成年後見の質問を取得"""
        return f"""📊 進捗: ステップ {self.step_count}/{self.total_steps}
成年後見制度についてお聞きします。

成年後見制度を利用していますか？
利用していない場合は「なし」と入力してください。"""

    def _get_service_questions(self) -> str:
        """サービス情報の質問を取得"""
        return f"""📊 進捗: ステップ {self.step_count}/{self.total_steps}
福祉サービスについてお聞きします。

現在利用しているサービスを教えてください。
（例: 生活介護、就労継続支援B型、グループホームなど）
利用していない場合は「なし」と入力してください。"""

    def _get_medical_questions(self) -> str:
        """医療情報の質問を取得"""
        return f"""📊 進捗: ステップ {self.step_count}/{self.total_steps}
医療機関についてお聞きします。

通院している医療機関を教えてください。
通院していない場合は「なし」と入力してください。

全ての情報入力が完了した場合は「完了」と入力してください。"""

    def _parse_date(self, date_str: str) -> Optional[str]:
        """
        日付文字列をパース

        Args:
            date_str: 日付文字列

        Returns:
            Optional[str]: YYYY-MM-DD形式の日付、または None
        """
        # 西暦形式（YYYY-MM-DD, YYYY/MM/DD, YYYY年MM月DD日）
        patterns = [
            r'(\d{4})-(\d{1,2})-(\d{1,2})',
            r'(\d{4})/(\d{1,2})/(\d{1,2})',
            r'(\d{4})年(\d{1,2})月(\d{1,2})日'
        ]

        for pattern in patterns:
            match = re.search(pattern, date_str)
            if match:
                year, month, day = match.groups()
                return f"{year}-{int(month):02d}-{int(day):02d}"

        # 元号形式（簡易実装）
        wareki_patterns = {
            "令和": 2018,
            "平成": 1988,
            "昭和": 1925
        }

        for era, base_year in wareki_patterns.items():
            pattern = f"{era}(\\d{{1,2}})年(\\d{{1,2}})月(\\d{{1,2}})日"
            match = re.search(pattern, date_str)
            if match:
                era_year, month, day = match.groups()
                year = base_year + int(era_year)
                return f"{year}-{int(month):02d}-{int(day):02d}"

        return None

    def _calculate_age(self, birth_date: str) -> int:
        """
        年齢を計算

        Args:
            birth_date: 生年月日（YYYY-MM-DD形式）

        Returns:
            int: 年齢
        """
        birth = datetime.strptime(birth_date, "%Y-%m-%d")
        today = datetime.now()
        age = today.year - birth.year
        if (today.month, today.day) < (birth.month, birth.day):
            age -= 1
        return age

    def _generate_summary(self) -> str:
        """収集したデータのサマリーを生成"""
        person = self.collected_data["person"]
        summary = f"""✅ データ収集が完了しました！

【本人情報】
- 氏名: {person.get('name', '未設定')}
- 生年月日: {person.get('birth_date', '未設定')} ({person.get('age', '未設定')}歳)
- 性別: {person.get('gender', '未設定')}

【家族】
- {len(self.collected_data['family'])}名

エコマップを生成しています...
"""
        return summary

    def get_collected_data(self) -> Dict[str, Any]:
        """
        収集したデータを取得

        Returns:
            Dict[str, Any]: 収集したデータ
        """
        return self.collected_data

    def is_complete(self) -> bool:
        """
        データ収集が完了したかチェック

        Returns:
            bool: 完了している場合 True
        """
        return self.state == DialogState.COMPLETE
