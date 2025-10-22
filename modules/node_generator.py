#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ノード生成モジュール

18種類のノードを生成します。
"""

import uuid
from datetime import datetime
from typing import Dict, List, Any


class NodeGenerator:
    """ノード生成クラス"""
    
    # ノードタイプと表示設定のマッピング
    NODE_DISPLAY_CONFIG = {
        "Person": {"color": "orange", "size": "large", "shape": "circle"},
        "Family": {"color": "red", "size": "medium", "shape": "circle"},
        "RyoikuNotebook": {"color": "darkred", "size": "medium", "shape": "circle"},
        "MentalHealthNotebook": {"color": "darkgreen", "size": "medium", "shape": "circle"},
        "PhysicalDisabilityNotebook": {"color": "darkblue", "size": "medium", "shape": "circle"},
        "SupportLevel": {"color": "purple", "size": "medium", "shape": "circle"},
        "Diagnosis": {"color": "lightblue", "size": "small", "shape": "circle"},
        "LegalGuardian": {"color": "brown", "size": "medium", "shape": "circle"},
        "ConsultationSupport": {"color": "purple", "size": "medium", "shape": "circle"},
        "ConsultationSupportSpecialist": {"color": "blue", "size": "small", "shape": "circle"},
        "ServicePlan": {"color": "blueviolet", "size": "medium", "shape": "circle"},
        "SupportService": {"color": "green", "size": "medium", "shape": "circle"},
        "ServiceManager": {"color": "green", "size": "small", "shape": "circle"},
        "ServiceContract": {"color": "green", "size": "medium", "shape": "circle"},
        "MedicalInstitution": {"color": "lightblue", "size": "medium", "shape": "circle"},
        "Doctor": {"color": "lightblue", "size": "small", "shape": "circle"},
        "Government": {"color": "gray", "size": "medium", "shape": "circle"},
        "Medication": {"color": "pink", "size": "small", "shape": "circle"},
    }
    
    def __init__(self):
        """初期化"""
        self.generated_nodes = {}  # ノードIDのキャッシュ（重複チェック用）
    
    def generate_person_node(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        本人ノードを生成
        
        Args:
            data: 本人情報データ
            
        Returns:
            ノード辞書
        """
        node_id = str(uuid.uuid4())
        
        node = {
            "id": node_id,
            "type": "Person",
            "name": data.get("name", ""),
            "properties": {
                "birth_date": data.get("birth_date", ""),
                "age": data.get("age", 0),
                "gender": data.get("gender", ""),
                "address": data.get("address", ""),
                "postal_code": data.get("postal_code", ""),
                "phone": data.get("phone", ""),
                "emergency_contact": data.get("emergency_contact", ""),
                "notes": data.get("notes", ""),
            },
            "display": self._get_display_config("Person", data.get("name", "")),
            "layer": "person",
            "is_default_visible": True,
            "created_at": datetime.now().isoformat(),
        }
        
        self.generated_nodes[node_id] = node
        return node
    
    def generate_family_node(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        家族ノードを生成
        
        Args:
            data: 家族情報データ
            
        Returns:
            ノード辞書
        """
        node_id = str(uuid.uuid4())
        
        # 同居・主介護者フラグから表示制御
        living_together = data.get("living_together", "") in ["○", "Yes", "yes"]
        primary_caregiver = data.get("primary_caregiver", "") in ["○", "Yes", "yes"]
        is_default_visible = living_together or primary_caregiver
        
        node = {
            "id": node_id,
            "type": "Family",
            "name": data.get("name", ""),
            "properties": {
                "relation": data.get("relation", ""),
                "birth_date": data.get("birth_date", ""),
                "age": data.get("age", 0),
                "gender": data.get("gender", ""),
                "living_together": living_together,
                "primary_caregiver": primary_caregiver,
                "address": data.get("address", ""),
                "phone": data.get("phone", ""),
                "notes": data.get("notes", ""),
            },
            "display": self._get_display_config("Family", data.get("name", "")),
            "layer": "family",
            "is_default_visible": is_default_visible,
            "created_at": datetime.now().isoformat(),
        }
        
        self.generated_nodes[node_id] = node
        return node
    
    def generate_notebook_node(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        手帳ノードを生成
        
        Args:
            data: 手帳情報データ
            
        Returns:
            ノード辞書
        """
        node_id = str(uuid.uuid4())
        
        # 手帳種別からノードタイプを決定
        notebook_type = data.get("type", "")
        if "療育" in notebook_type:
            node_type = "RyoikuNotebook"
        elif "精神" in notebook_type:
            node_type = "MentalHealthNotebook"
        elif "身体" in notebook_type:
            node_type = "PhysicalDisabilityNotebook"
        else:
            node_type = "RyoikuNotebook"  # デフォルト
        
        # 状態から表示制御（有効なもののみデフォルト表示）
        is_default_visible = data.get("status", "") == "有効"
        
        node = {
            "id": node_id,
            "type": node_type,
            "name": f"{notebook_type} {data.get('grade', '')}",
            "properties": {
                "type": notebook_type,
                "grade": data.get("grade", ""),
                "number": data.get("number", ""),
                "issue_date": data.get("issue_date", ""),
                "expiry_date": data.get("expiry_date", ""),
                "issuing_authority": data.get("issuing_authority", ""),
                "status": data.get("status", ""),
                "notes": data.get("notes", ""),
            },
            "display": self._get_display_config(node_type, f"{notebook_type} {data.get('grade', '')}"),
            "layer": "notebooks",
            "is_default_visible": is_default_visible,
            "created_at": datetime.now().isoformat(),
        }
        
        self.generated_nodes[node_id] = node
        return node
    
    def generate_support_level_node(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        支援区分ノードを生成
        
        Args:
            data: 支援区分情報データ
            
        Returns:
            ノード辞書
        """
        node_id = str(uuid.uuid4())
        
        # 状態から表示制御（現在のもののみデフォルト表示）
        is_default_visible = data.get("status", "") == "現在"
        
        node = {
            "id": node_id,
            "type": "SupportLevel",
            "name": f"支援区分{data.get('level', '')}",
            "properties": {
                "level": data.get("level", 0),
                "decision_date": data.get("decision_date", ""),
                "expiry_date": data.get("expiry_date", ""),
                "deciding_authority": data.get("deciding_authority", ""),
                "assessor": data.get("assessor", ""),
                "status": data.get("status", ""),
                "notes": data.get("notes", ""),
            },
            "display": self._get_display_config("SupportLevel", f"区分{data.get('level', '')}"),
            "layer": "support_levels",
            "is_default_visible": is_default_visible,
            "created_at": datetime.now().isoformat(),
        }
        
        self.generated_nodes[node_id] = node
        return node
    
    def generate_diagnosis_node(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        診断ノードを生成
        
        Args:
            data: 診断情報データ
            
        Returns:
            ノード辞書
        """
        node_id = str(uuid.uuid4())
        
        node = {
            "id": node_id,
            "type": "Diagnosis",
            "name": data.get("name", ""),
            "properties": {
                "name": data.get("name", ""),
                "icd10_code": data.get("icd10_code", ""),
                "diagnosis_date": data.get("diagnosis_date", ""),
                "doctor": data.get("doctor", ""),
                "institution": data.get("institution", ""),
                "status": data.get("status", ""),
                "notes": data.get("notes", ""),
            },
            "display": self._get_display_config("Diagnosis", data.get("name", "")),
            "layer": "diagnoses",
            "is_default_visible": False,  # デフォルトは非表示
            "created_at": datetime.now().isoformat(),
        }
        
        self.generated_nodes[node_id] = node
        return node
    
    def generate_legal_guardian_node(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        成年後見人ノードを生成
        
        Args:
            data: 成年後見情報データ
            
        Returns:
            ノード辞書
        """
        node_id = str(uuid.uuid4())
        
        node = {
            "id": node_id,
            "type": "LegalGuardian",
            "name": data.get("name", ""),
            "properties": {
                "name": data.get("name", ""),
                "type": data.get("type", ""),
                "category": data.get("category", ""),
                "profession": data.get("profession", ""),
                "start_date": data.get("start_date", ""),
                "authority": data.get("authority", ""),
                "contact": data.get("contact", ""),
                "notes": data.get("notes", ""),
            },
            "display": self._get_display_config("LegalGuardian", data.get("name", "")),
            "layer": "legal_guardians",
            "is_default_visible": True,  # デフォルト表示
            "created_at": datetime.now().isoformat(),
        }
        
        self.generated_nodes[node_id] = node
        return node
    
    def generate_consultation_support_node(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        相談支援事業所ノードを生成
        
        Args:
            data: 相談支援情報データ
            
        Returns:
            ノード辞書
        """
        node_id = str(uuid.uuid4())
        
        node = {
            "id": node_id,
            "type": "ConsultationSupport",
            "name": data.get("office_name", ""),
            "properties": {
                "office_name": data.get("office_name", ""),
                "office_number": data.get("office_number", ""),
                "support_type": data.get("support_type", ""),
                "address": data.get("address", ""),
                "phone": data.get("phone", ""),
                "contract_date": data.get("contract_date", ""),
                "notes": data.get("notes", ""),
            },
            "display": self._get_display_config("ConsultationSupport", data.get("office_name", "")),
            "layer": "consultation_supports",
            "is_default_visible": False,  # デフォルトは非表示
            "created_at": datetime.now().isoformat(),
        }
        
        self.generated_nodes[node_id] = node
        return node
    
    def generate_consultation_support_specialist_node(self, name: str, office_id: str) -> Dict[str, Any]:
        """
        相談支援専門員ノードを生成
        
        Args:
            name: 専門員氏名
            office_id: 所属事業所のノードID
            
        Returns:
            ノード辞書
        """
        node_id = str(uuid.uuid4())
        
        node = {
            "id": node_id,
            "type": "ConsultationSupportSpecialist",
            "name": name,
            "properties": {
                "name": name,
                "office_id": office_id,
            },
            "display": self._get_display_config("ConsultationSupportSpecialist", name),
            "layer": "consultation_supports",
            "is_default_visible": False,
            "created_at": datetime.now().isoformat(),
        }
        
        self.generated_nodes[node_id] = node
        return node
    
    def generate_service_plan_node(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        サービス等利用計画ノードを生成
        
        Args:
            data: サービス等利用計画情報データ
            
        Returns:
            ノード辞書
        """
        node_id = str(uuid.uuid4())
        
        # 状態から表示制御（有効なもののみデフォルト表示）
        is_default_visible = data.get("status", "") == "有効"
        
        plan_name = f"サービス等利用計画"
        if data.get("plan_number"):
            plan_name += f" {data.get('plan_number')}"
        
        node = {
            "id": node_id,
            "type": "ServicePlan",
            "name": plan_name,
            "properties": {
                "plan_number": data.get("plan_number", ""),
                "creation_date": data.get("creation_date", ""),
                "last_monitoring_date": data.get("last_monitoring_date", ""),
                "next_monitoring_date": data.get("next_monitoring_date", ""),
                "status": data.get("status", ""),
                "notes": data.get("notes", ""),
            },
            "display": self._get_display_config("ServicePlan", plan_name),
            "layer": "service_plans",
            "is_default_visible": is_default_visible,
            "created_at": datetime.now().isoformat(),
        }
        
        self.generated_nodes[node_id] = node
        return node
    
    def generate_support_service_node(self, office_name: str, office_number: str = "") -> Dict[str, Any]:
        """
        福祉サービス事業所ノードを生成
        
        Args:
            office_name: 事業所名
            office_number: 事業所番号
            
        Returns:
            ノード辞書
        """
        node_id = str(uuid.uuid4())
        
        node = {
            "id": node_id,
            "type": "SupportService",
            "name": office_name,
            "properties": {
                "office_name": office_name,
                "office_number": office_number,
            },
            "display": self._get_display_config("SupportService", office_name),
            "layer": "service_contracts",
            "is_default_visible": True,
            "created_at": datetime.now().isoformat(),
        }
        
        self.generated_nodes[node_id] = node
        return node
    
    def generate_service_manager_node(self, name: str, office_id: str) -> Dict[str, Any]:
        """
        サービス管理責任者ノードを生成
        
        Args:
            name: 管理責任者氏名
            office_id: 所属事業所のノードID
            
        Returns:
            ノード辞書
        """
        node_id = str(uuid.uuid4())
        
        node = {
            "id": node_id,
            "type": "ServiceManager",
            "name": name,
            "properties": {
                "name": name,
                "office_id": office_id,
            },
            "display": self._get_display_config("ServiceManager", name),
            "layer": "service_contracts",
            "is_default_visible": False,
            "created_at": datetime.now().isoformat(),
        }
        
        self.generated_nodes[node_id] = node
        return node
    
    def generate_service_contract_node(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        サービス利用契約ノードを生成
        
        Args:
            data: サービス利用情報データ
            
        Returns:
            ノード辞書
        """
        node_id = str(uuid.uuid4())
        
        # 状態から表示制御（契約中のもののみデフォルト表示）
        is_default_visible = data.get("status", "") == "契約中"
        
        node = {
            "id": node_id,
            "type": "ServiceContract",
            "name": f"{data.get('service_type', '')} 契約",
            "properties": {
                "service_type": data.get("service_type", ""),
                "contract_date": data.get("contract_date", ""),
                "frequency": data.get("frequency", ""),
                "days": data.get("days", ""),
                "status": data.get("status", ""),
                "notes": data.get("notes", ""),
            },
            "display": self._get_display_config("ServiceContract", data.get("service_type", "")),
            "layer": "service_contracts",
            "is_default_visible": is_default_visible,
            "created_at": datetime.now().isoformat(),
        }
        
        self.generated_nodes[node_id] = node
        return node
    
    def generate_medical_institution_node(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        医療機関ノードを生成
        
        Args:
            data: 医療機関情報データ
            
        Returns:
            ノード辞書
        """
        node_id = str(uuid.uuid4())
        
        node = {
            "id": node_id,
            "type": "MedicalInstitution",
            "name": data.get("name", ""),
            "properties": {
                "name": data.get("name", ""),
                "department": data.get("department", ""),
                "address": data.get("address", ""),
                "phone": data.get("phone", ""),
                "start_date": data.get("start_date", ""),
                "frequency": data.get("frequency", ""),
                "treatment": data.get("treatment", ""),
                "notes": data.get("notes", ""),
            },
            "display": self._get_display_config("MedicalInstitution", data.get("name", "")),
            "layer": "medical",
            "is_default_visible": False,
            "created_at": datetime.now().isoformat(),
        }
        
        self.generated_nodes[node_id] = node
        return node
    
    def generate_doctor_node(self, name: str, institution_id: str) -> Dict[str, Any]:
        """
        医師ノードを生成
        
        Args:
            name: 医師氏名
            institution_id: 所属医療機関のノードID
            
        Returns:
            ノード辞書
        """
        node_id = str(uuid.uuid4())
        
        node = {
            "id": node_id,
            "type": "Doctor",
            "name": name,
            "properties": {
                "name": name,
                "institution_id": institution_id,
            },
            "display": self._get_display_config("Doctor", name),
            "layer": "medical",
            "is_default_visible": False,
            "created_at": datetime.now().isoformat(),
        }
        
        self.generated_nodes[node_id] = node
        return node
    
    def generate_medication_node(self, medication_str: str, doctor_id: str) -> List[Dict[str, Any]]:
        """
        処方薬ノードを生成（複数の薬を解析）
        
        Args:
            medication_str: 処方薬文字列（例: "リスペリドン2mg 朝夕、バルプロ酸200mg 朝昼夕"）
            doctor_id: 処方医のノードID
            
        Returns:
            ノードのリスト
        """
        if not medication_str:
            return []
        
        nodes = []
        
        # カンマまたは読点で分割
        medications = [m.strip() for m in medication_str.replace("、", ",").split(",")]
        
        for med in medications:
            if not med:
                continue
            
            node_id = str(uuid.uuid4())
            
            node = {
                "id": node_id,
                "type": "Medication",
                "name": med,
                "properties": {
                    "medication": med,
                    "doctor_id": doctor_id,
                },
                "display": self._get_display_config("Medication", med),
                "layer": "medical",
                "is_default_visible": False,
                "created_at": datetime.now().isoformat(),
            }
            
            self.generated_nodes[node_id] = node
            nodes.append(node)
        
        return nodes
    
    def _get_display_config(self, node_type: str, label: str) -> Dict[str, Any]:
        """
        表示設定を取得
        
        Args:
            node_type: ノードタイプ
            label: 表示ラベル
            
        Returns:
            表示設定辞書
        """
        config = self.NODE_DISPLAY_CONFIG.get(node_type, {
            "color": "gray",
            "size": "medium",
            "shape": "circle"
        })
        
        return {
            "color": config["color"],
            "size": config["size"],
            "shape": config["shape"],
            "label": label,
        }


if __name__ == "__main__":
    print("=== NodeGenerator テスト ===")
    
    generator = NodeGenerator()
    
    # 本人ノード
    print("\n【本人ノード】")
    person = generator.generate_person_node({
        "name": "山田太郎",
        "birth_date": "2000-01-01",
        "age": 25,
        "gender": "男"
    })
    print(f"ID: {person['id']}")
    print(f"タイプ: {person['type']}")
    print(f"名前: {person['name']}")
    print(f"表示: {person['display']}")
    
    # 家族ノード
    print("\n【家族ノード】")
    family = generator.generate_family_node({
        "name": "山田花子",
        "relation": "母",
        "living_together": "○",
        "primary_caregiver": "○"
    })
    print(f"名前: {family['name']}")
    print(f"デフォルト表示: {family['is_default_visible']}")
    
    # 手帳ノード
    print("\n【手帳ノード】")
    notebook = generator.generate_notebook_node({
        "type": "療育手帳",
        "grade": "A1",
        "status": "有効"
    })
    print(f"名前: {notebook['name']}")
    print(f"タイプ: {notebook['type']}")
    
    print(f"\n生成したノード数: {len(generator.generated_nodes)}")
