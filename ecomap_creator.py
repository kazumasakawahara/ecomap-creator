#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
エコマップ作成スキル - メインスクリプト

Excelファイルから支援情報を読み込み、エコマップ（JSON + HTML）を生成します。
"""

import sys
import os
import argparse
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple

# モジュールをインポート
from modules.excel_reader import ExcelReader
from modules.date_converter import DateConverter
from modules.validator import Validator
from modules.node_generator import NodeGenerator
from modules.relation_generator import RelationGenerator
from modules.html_generator import HTMLGenerator
from modules.interactive_dialog import InteractiveDialogEngine


class EcomapCreator:
    """エコマップ作成クラス"""

    VERSION = "1.1.0"
    
    def __init__(
        self,
        input_file: str = None,
        output_dir: str = "outputs",
        visualization: str = "d3",
        debug: bool = False,
        interactive: bool = False
    ):
        """
        初期化

        Args:
            input_file: 入力Excelファイルパス（対話モードでは不要）
            output_dir: 出力ディレクトリ
            visualization: 可視化ライブラリ（"d3" or "cytoscape"）
            debug: デバッグモード
            interactive: 対話モード
        """
        self.input_file = input_file
        self.output_dir = output_dir
        self.visualization = visualization
        self.debug = debug
        self.interactive = interactive

        # ロガーの設定
        self._setup_logger()

        # 出力ディレクトリの作成
        os.makedirs(output_dir, exist_ok=True)

        # 対話モードの場合、対話エンジンを初期化
        if interactive:
            self.dialog_engine = InteractiveDialogEngine()
    
    def _setup_logger(self):
        """ロガーの設定"""
        level = logging.DEBUG if self.debug else logging.INFO
        
        logging.basicConfig(
            level=level,
            format='[%(levelname)s] %(message)s'
        )
        
        self.logger = logging.getLogger(__name__)

    def _run_interactive_mode(self) -> Tuple[str, str]:
        """
        対話モードで実行

        Returns:
            (JSONファイルパス, HTMLファイルパス)
        """
        self.logger.info("対話モードでエコマップ作成を開始します")

        # 対話エンジンを使用してデータ収集
        print("\nNote: 対話モードはClaude Desktop内での使用を想定しています。")
        print("コマンドラインでの対話は制限されます。\n")

        # データ収集が完了したか確認
        if not self.dialog_engine.is_complete():
            raise RuntimeError(
                "対話モードでの使用には、Claude Desktop経由で実行してください。\n"
                "コマンドラインでの対話データ収集は現在サポートされていません。"
            )

        # 収集したデータを取得
        data = self.dialog_engine.get_collected_data()

        # データ検証
        self.logger.info("データを検証しています...")
        errors = self._validate_data(data)
        if errors:
            self.logger.warning("データ検証で警告がありました:")
            for error in errors:
                self.logger.warning(f"  {error}")

        # 日付変換
        self.logger.info("日付を変換しています...")
        data = self._convert_dates(data)

        # ノード生成
        self.logger.info("ノードを生成しています...")
        nodes = self._generate_nodes(data)
        self.logger.info(f"  ノード数: {len(nodes)}")

        # リレーション生成
        self.logger.info("リレーションを生成しています...")
        relations = self._generate_relations(data, nodes)
        self.logger.info(f"  リレーション数: {len(relations)}")

        # JSONファイル生成
        self.logger.info("JSONファイルを生成しています...")
        json_path = self._generate_json(data, nodes, relations)
        self.logger.info(f"  JSONファイル: {json_path}")

        # HTMLファイル生成
        self.logger.info("HTMLファイルを生成しています...")
        html_path = self._generate_html(data, nodes, relations)
        self.logger.info(f"  HTMLファイル: {html_path}")

        self.logger.info("✓ エコマップの作成が完了しました！")

        return json_path, html_path

    def run(self) -> Tuple[str, str]:
        """
        メイン処理を実行

        Returns:
            (JSONファイルパス, HTMLファイルパス)
        """
        try:
            # 対話モードの場合
            if self.interactive:
                return self._run_interactive_mode()

            # ファイルモードの場合
            self.logger.info(f"エコマップ作成を開始します: {self.input_file}")

            # 1. Excelファイル読み込み
            self.logger.info("Excelファイルを読み込んでいます...")
            data = self._load_excel()
            self.logger.debug(f"読み込んだデータ: 本人={data['person'].get('name')}")

            # 2. データ検証
            self.logger.info("データを検証しています...")
            errors = self._validate_data(data)
            if errors:
                self.logger.error("データ検証エラー:")
                for error in errors:
                    self.logger.error(f"  {error}")
                raise ValueError("データ検証に失敗しました")

            # 3. 日付変換
            self.logger.info("日付を変換しています...")
            data = self._convert_dates(data)
            self.logger.debug(f"本人年齢: {data['person'].get('age')}歳")
            
            # 4. ノード生成
            self.logger.info("ノードを生成しています...")
            nodes = self._generate_nodes(data)
            self.logger.info(f"  ノード数: {len(nodes)}")
            
            # 5. リレーション生成
            self.logger.info("リレーションを生成しています...")
            relations = self._generate_relations(data, nodes)
            self.logger.info(f"  リレーション数: {len(relations)}")
            
            # 6. JSONファイル生成
            self.logger.info("JSONファイルを生成しています...")
            json_path = self._generate_json(data, nodes, relations)
            self.logger.info(f"  JSONファイル: {json_path}")
            
            # 7. HTMLファイル生成
            self.logger.info("HTMLファイルを生成しています...")
            html_path = self._generate_html(data, nodes, relations)
            self.logger.info(f"  HTMLファイル: {html_path}")
            
            self.logger.info("✓ エコマップの作成が完了しました！")
            
            return json_path, html_path
            
        except Exception as e:
            self.logger.error(f"エラーが発生しました: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
            raise
    
    def _load_excel(self) -> Dict[str, Any]:
        """Excelファイルを読み込み"""
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"ファイルが見つかりません: {self.input_file}")
        
        reader = ExcelReader(self.input_file)
        return reader.load()
    
    def _validate_data(self, data: Dict[str, Any]) -> List[str]:
        """データを検証"""
        return Validator.validate_all_data(data)
    
    def _convert_dates(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """日付を変換"""
        converter = DateConverter()
        
        # 本人の生年月日を変換
        if data["person"].get("birth_date"):
            data["person"]["birth_date"] = converter.normalize_date(data["person"]["birth_date"])
            data["person"]["age"] = converter.calculate_age(data["person"]["birth_date"])
        
        # 家族の生年月日を変換
        for family in data.get("family", []):
            if family.get("birth_date"):
                family["birth_date"] = converter.normalize_date(family["birth_date"])
                family["age"] = converter.calculate_age(family["birth_date"])
        
        # 手帳情報の日付を変換
        for notebook in data.get("notebooks", []):
            if notebook.get("issue_date"):
                notebook["issue_date"] = converter.normalize_date(notebook["issue_date"])
            if notebook.get("expiry_date"):
                notebook["expiry_date"] = converter.normalize_date(notebook["expiry_date"])
        
        # 支援区分情報の日付を変換
        for level in data.get("support_levels", []):
            if level.get("decision_date"):
                level["decision_date"] = converter.normalize_date(level["decision_date"])
            if level.get("expiry_date"):
                level["expiry_date"] = converter.normalize_date(level["expiry_date"])
        
        # 診断情報の日付を変換
        for diagnosis in data.get("diagnoses", []):
            if diagnosis.get("diagnosis_date"):
                diagnosis["diagnosis_date"] = converter.normalize_date(diagnosis["diagnosis_date"])
        
        # 成年後見情報の日付を変換
        for guardian in data.get("legal_guardians", []):
            if guardian.get("start_date"):
                guardian["start_date"] = converter.normalize_date(guardian["start_date"])
        
        # 相談支援情報の日付を変換
        for support in data.get("consultation_supports", []):
            if support.get("contract_date"):
                support["contract_date"] = converter.normalize_date(support["contract_date"])
        
        # サービス等利用計画の日付を変換
        for plan in data.get("service_plans", []):
            if plan.get("creation_date"):
                plan["creation_date"] = converter.normalize_date(plan["creation_date"])
            if plan.get("last_monitoring_date"):
                plan["last_monitoring_date"] = converter.normalize_date(plan["last_monitoring_date"])
            if plan.get("next_monitoring_date"):
                plan["next_monitoring_date"] = converter.normalize_date(plan["next_monitoring_date"])
        
        # サービス利用情報の日付を変換
        for contract in data.get("service_contracts", []):
            if contract.get("contract_date"):
                contract["contract_date"] = converter.normalize_date(contract["contract_date"])
        
        # 医療機関情報の日付を変換
        for institution in data.get("medical_institutions", []):
            if institution.get("start_date"):
                institution["start_date"] = converter.normalize_date(institution["start_date"])
        
        return data
    
    def _generate_nodes(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """ノードを生成"""
        generator = NodeGenerator()
        nodes = []
        
        # 本人ノード（必須）
        person_node = generator.generate_person_node(data["person"])
        nodes.append(person_node)
        
        # 家族ノード
        for family in data.get("family", []):
            node = generator.generate_family_node(family)
            nodes.append(node)
        
        # 手帳ノード
        for notebook in data.get("notebooks", []):
            node = generator.generate_notebook_node(notebook)
            nodes.append(node)
        
        # 支援区分ノード
        for level in data.get("support_levels", []):
            node = generator.generate_support_level_node(level)
            nodes.append(node)
        
        # 診断ノード
        for diagnosis in data.get("diagnoses", []):
            node = generator.generate_diagnosis_node(diagnosis)
            nodes.append(node)
        
        # 成年後見人ノード
        for guardian in data.get("legal_guardians", []):
            node = generator.generate_legal_guardian_node(guardian)
            nodes.append(node)
        
        # 相談支援事業所ノード
        for support in data.get("consultation_supports", []):
            office_node = generator.generate_consultation_support_node(support)
            nodes.append(office_node)
            
            # 相談支援専門員ノード
            if support.get("specialist"):
                specialist_node = generator.generate_consultation_support_specialist_node(
                    support["specialist"],
                    office_node["id"]
                )
                nodes.append(specialist_node)
        
        # サービス等利用計画ノード
        for plan in data.get("service_plans", []):
            node = generator.generate_service_plan_node(plan)
            nodes.append(node)
        
        # サービス利用情報ノード
        for contract in data.get("service_contracts", []):
            # サービス契約ノード
            contract_node = generator.generate_service_contract_node(contract)
            nodes.append(contract_node)
            
            # 福祉サービス事業所ノード
            if contract.get("office_name"):
                service_node = generator.generate_support_service_node(
                    contract["office_name"],
                    contract.get("office_number", "")
                )
                nodes.append(service_node)
            
            # サービス管理責任者ノード
            if contract.get("manager") and contract.get("office_name"):
                manager_node = generator.generate_service_manager_node(
                    contract["manager"],
                    service_node["id"]
                )
                nodes.append(manager_node)
        
        # 医療機関情報ノード
        for institution in data.get("medical_institutions", []):
            institution_node = generator.generate_medical_institution_node(institution)
            nodes.append(institution_node)
            
            # 医師ノード
            if institution.get("doctor"):
                doctor_node = generator.generate_doctor_node(
                    institution["doctor"],
                    institution_node["id"]
                )
                nodes.append(doctor_node)
                
                # 処方薬ノード
                if institution.get("medications"):
                    medication_nodes = generator.generate_medication_node(
                        institution["medications"],
                        doctor_node["id"]
                    )
                    nodes.extend(medication_nodes)
        
        return nodes
    
    def _generate_relations(self, data: Dict[str, Any], nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """リレーションを生成"""
        generator = RelationGenerator()
        
        # ノードIDのマップを作成
        person_node = next(n for n in nodes if n["type"] == "Person")
        
        # 家族リレーション
        family_nodes = [n for n in nodes if n["type"] == "Family"]
        family_data_list = data.get("family", [])
        for i, family_node in enumerate(family_nodes):
            if i < len(family_data_list):
                generator.generate_family_relation(
                    person_node["id"],
                    family_node["id"],
                    family_data_list[i].get("relation", "")
                )
        
        # 手帳リレーション
        notebook_nodes = [n for n in nodes if "Notebook" in n["type"]]
        for notebook_node in notebook_nodes:
            generator.generate_has_notebook_relation(
                person_node["id"],
                notebook_node["id"]
            )
        
        # 支援区分リレーション
        support_level_nodes = [n for n in nodes if n["type"] == "SupportLevel"]
        for level_node in support_level_nodes:
            generator.generate_has_support_level_relation(
                person_node["id"],
                level_node["id"]
            )
        
        # 診断リレーション
        diagnosis_nodes = [n for n in nodes if n["type"] == "Diagnosis"]
        for diagnosis_node in diagnosis_nodes:
            generator.generate_has_diagnosis_relation(
                person_node["id"],
                diagnosis_node["id"]
            )
        
        # 成年後見リレーション
        guardian_nodes = [n for n in nodes if n["type"] == "LegalGuardian"]
        for guardian_node in guardian_nodes:
            generator.generate_under_guardianship_relation(
                person_node["id"],
                guardian_node["id"]
            )
        
        # 相談支援リレーション
        consultation_offices = [n for n in nodes if n["type"] == "ConsultationSupport"]
        consultation_specialists = [n for n in nodes if n["type"] == "ConsultationSupportSpecialist"]
        for specialist in consultation_specialists:
            office_id = specialist["properties"]["office_id"]
            generator.generate_works_for_relation(specialist["id"], office_id)
        
        # サービス等利用計画リレーション
        service_plans = [n for n in nodes if n["type"] == "ServicePlan"]
        for plan in service_plans:
            generator.generate_has_service_plan_relation(
                person_node["id"],
                plan["id"]
            )
            
            # 作成者リレーション（専門員がいる場合）
            if consultation_specialists:
                generator.generate_created_by_relation(
                    plan["id"],
                    consultation_specialists[0]["id"]
                )
        
        # サービス契約リレーション
        service_contracts = [n for n in nodes if n["type"] == "ServiceContract"]
        support_services = [n for n in nodes if n["type"] == "SupportService"]
        service_managers = [n for n in nodes if n["type"] == "ServiceManager"]
        
        for contract in service_contracts:
            # 本人→契約
            generator.generate_has_contract_relation(
                person_node["id"],
                contract["id"]
            )
            
            # 契約→事業所（事業所名でマッチング）
            for service in support_services:
                generator.generate_contract_with_relation(
                    contract["id"],
                    service["id"]
                )
                break
            
            # 契約→管理責任者
            for manager in service_managers:
                generator.generate_managed_by_relation(
                    contract["id"],
                    manager["id"]
                )
                
                # 管理責任者→事業所
                for service in support_services:
                    generator.generate_works_for_relation(
                        manager["id"],
                        service["id"]
                    )
                    break
                break
        
        # 医療機関リレーション
        medical_institutions = [n for n in nodes if n["type"] == "MedicalInstitution"]
        doctors = [n for n in nodes if n["type"] == "Doctor"]
        medications = [n for n in nodes if n["type"] == "Medication"]
        
        for institution in medical_institutions:
            # 本人→医療機関
            generator.generate_receives_medical_care_relation(
                person_node["id"],
                institution["id"]
            )
        
        for doctor in doctors:
            # 本人→医師
            generator.generate_treated_by_relation(
                person_node["id"],
                doctor["id"]
            )
            
            # 医師→医療機関
            institution_id = doctor["properties"]["institution_id"]
            generator.generate_works_for_relation(
                doctor["id"],
                institution_id
            )
        
        for medication in medications:
            # 本人→処方薬
            generator.generate_takes_medication_relation(
                person_node["id"],
                medication["id"]
            )
            
            # 処方薬→医師
            doctor_id = medication["properties"]["doctor_id"]
            generator.generate_prescribed_by_relation(
                medication["id"],
                doctor_id
            )
        
        return generator.generated_relations
    
    def _generate_json(self, data: Dict[str, Any], nodes: List[Dict[str, Any]], relations: List[Dict[str, Any]]) -> str:
        """JSONファイルを生成"""
        person_name = data["person"].get("name", "不明")
        person_age = data["person"].get("age", 0)
        
        json_data = {
            "person": {
                "id": nodes[0]["id"],
                "name": person_name,
                "age": person_age,
                "birth_date": data["person"].get("birth_date", ""),
                "gender": data["person"].get("gender", ""),
            },
            "nodes": nodes,
            "relations": relations,
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "created_by": f"ecomap-creator v{self.VERSION}",
                "version": self.VERSION,
                "schema_version": "1.0.0",
                "source_file": os.path.basename(self.input_file) if self.input_file else "interactive_mode",
                "node_count": len(nodes),
                "relation_count": len(relations),
                "person_name": person_name,
                "person_age": person_age,
            }
        }
        
        # ファイル名を生成
        json_filename = f"{person_name}_ecomap.json"
        json_path = os.path.join(self.output_dir, json_filename)
        
        # JSONファイルを保存
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        return json_path
    
    def _generate_html(self, data: Dict[str, Any], nodes: List[Dict[str, Any]], relations: List[Dict[str, Any]]) -> str:
        """HTMLファイルを生成"""
        person_name = data["person"].get("name", "不明")
        person_age = data["person"].get("age", 0)
        
        json_data = {
            "person": {
                "id": nodes[0]["id"],
                "name": person_name,
                "age": person_age,
            },
            "nodes": nodes,
            "relations": relations,
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "node_count": len(nodes),
                "relation_count": len(relations),
            }
        }
        
        generator = HTMLGenerator(self.visualization)
        html_content = generator.generate(json_data, person_name)
        
        # ファイル名を生成
        html_filename = f"{person_name}_ecomap.html"
        html_path = os.path.join(self.output_dir, html_filename)
        
        # HTMLファイルを保存
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return html_path


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="エコマップ作成スキル - 対話形式またはExcelファイルから支援情報を読み込み、エコマップを生成します"
    )

    parser.add_argument(
        "input_file",
        nargs="?",  # オプショナル引数に変更
        help="入力Excelファイルパス（省略すると対話モード）"
    )

    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="対話モードで実行"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="outputs",
        help="出力ディレクトリ（デフォルト: outputs）"
    )
    
    parser.add_argument(
        "-v", "--visualization",
        default="d3",
        choices=["d3", "cytoscape"],
        help="可視化ライブラリ（デフォルト: d3）"
    )
    
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="デバッグモード"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {EcomapCreator.VERSION}"
    )
    
    args = parser.parse_args()

    # モード判定: ファイルが指定されていない、または-iフラグがある場合は対話モード
    interactive_mode = args.interactive or (args.input_file is None and sys.stdin.isatty())

    if interactive_mode:
        print("=" * 60)
        print("エコマップ作成スキル - 対話モード")
        print("=" * 60)
        print("\nNote: このモードはClaude Desktop経由での使用を想定しています。")
        print("コマンドラインでは制限があります。")
        print("\n対話を開始するには、Claude Desktopで以下のように依頼してください：")
        print('「田中一郎さんのエコマップを作成してください」')
        print("\nまたは、Excelファイルを使用する場合:")
        print(f"  {sys.argv[0]} sample.xlsx")
        print("=" * 60)
        return 0

    # ファイルモード
    if not args.input_file:
        parser.print_help()
        print("\nエラー: 入力ファイルを指定するか、-iオプションで対話モードを使用してください。")
        return 1

    try:
        creator = EcomapCreator(
            input_file=args.input_file,
            output_dir=args.output,
            visualization=args.visualization,
            debug=args.debug,
            interactive=False
        )

        json_path, html_path = creator.run()

        print("\n" + "=" * 50)
        print("✓ エコマップの作成が完了しました！")
        print("=" * 50)
        print(f"JSONファイル: {json_path}")
        print(f"HTMLファイル: {html_path}")
        print("\nHTMLファイルをブラウザで開いてください。")

        return 0

    except Exception as e:
        print(f"\n✗ エラー: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
