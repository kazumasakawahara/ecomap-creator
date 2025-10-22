#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
リレーション生成モジュール

19種類のリレーションを生成します。
"""

import uuid
from datetime import datetime
from typing import Dict, List, Any


class RelationGenerator:
    """リレーション生成クラス"""
    
    def __init__(self):
        """初期化"""
        self.generated_relations = []
    
    def generate_has_notebook_relation(self, person_id: str, notebook_id: str) -> Dict[str, Any]:
        """
        HAS_NOTEBOOK リレーションを生成（本人→手帳）
        
        Args:
            person_id: 本人ノードID
            notebook_id: 手帳ノードID
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="HAS_NOTEBOOK",
            source_id=person_id,
            target_id=notebook_id,
            direction="directed",
            properties={},
            layer="notebooks"
        )
        return relation
    
    def generate_has_support_level_relation(self, person_id: str, support_level_id: str) -> Dict[str, Any]:
        """
        HAS_SUPPORT_LEVEL リレーションを生成（本人→支援区分）
        
        Args:
            person_id: 本人ノードID
            support_level_id: 支援区分ノードID
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="HAS_SUPPORT_LEVEL",
            source_id=person_id,
            target_id=support_level_id,
            direction="directed",
            properties={},
            layer="support_levels"
        )
        return relation
    
    def generate_has_diagnosis_relation(self, person_id: str, diagnosis_id: str) -> Dict[str, Any]:
        """
        HAS_DIAGNOSIS リレーションを生成（本人→診断）
        
        Args:
            person_id: 本人ノードID
            diagnosis_id: 診断ノードID
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="HAS_DIAGNOSIS",
            source_id=person_id,
            target_id=diagnosis_id,
            direction="directed",
            properties={},
            layer="diagnoses"
        )
        return relation
    
    def generate_family_relation(self, person_id: str, family_id: str, relation_type: str) -> Dict[str, Any]:
        """
        FAMILY_RELATION リレーションを生成（本人↔家族）
        
        Args:
            person_id: 本人ノードID
            family_id: 家族ノードID
            relation_type: 続柄（例: "母"、"父"）
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="FAMILY_RELATION",
            source_id=person_id,
            target_id=family_id,
            direction="undirected",
            properties={"relation": relation_type},
            layer="family"
        )
        return relation
    
    def generate_under_guardianship_relation(self, person_id: str, guardian_id: str) -> Dict[str, Any]:
        """
        UNDER_GUARDIANSHIP リレーションを生成（本人→成年後見人）
        
        Args:
            person_id: 本人ノードID
            guardian_id: 成年後見人ノードID
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="UNDER_GUARDIANSHIP",
            source_id=person_id,
            target_id=guardian_id,
            direction="directed",
            properties={},
            layer="legal_guardians"
        )
        return relation
    
    def generate_has_service_plan_relation(self, person_id: str, service_plan_id: str) -> Dict[str, Any]:
        """
        HAS_SERVICE_PLAN リレーションを生成（本人→サービス等利用計画）
        
        Args:
            person_id: 本人ノードID
            service_plan_id: サービス等利用計画ノードID
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="HAS_SERVICE_PLAN",
            source_id=person_id,
            target_id=service_plan_id,
            direction="directed",
            properties={},
            layer="service_plans"
        )
        return relation
    
    def generate_has_contract_relation(self, person_id: str, contract_id: str) -> Dict[str, Any]:
        """
        HAS_CONTRACT リレーションを生成（本人→サービス契約）
        
        Args:
            person_id: 本人ノードID
            contract_id: サービス契約ノードID
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="HAS_CONTRACT",
            source_id=person_id,
            target_id=contract_id,
            direction="directed",
            properties={},
            layer="service_contracts"
        )
        return relation
    
    def generate_receives_medical_care_relation(self, person_id: str, institution_id: str) -> Dict[str, Any]:
        """
        RECEIVES_MEDICAL_CARE リレーションを生成（本人→医療機関）
        
        Args:
            person_id: 本人ノードID
            institution_id: 医療機関ノードID
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="RECEIVES_MEDICAL_CARE",
            source_id=person_id,
            target_id=institution_id,
            direction="directed",
            properties={},
            layer="medical"
        )
        return relation
    
    def generate_treated_by_relation(self, person_id: str, doctor_id: str) -> Dict[str, Any]:
        """
        TREATED_BY リレーションを生成（本人→医師）
        
        Args:
            person_id: 本人ノードID
            doctor_id: 医師ノードID
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="TREATED_BY",
            source_id=person_id,
            target_id=doctor_id,
            direction="directed",
            properties={},
            layer="medical"
        )
        return relation
    
    def generate_created_by_relation(self, service_plan_id: str, specialist_id: str) -> Dict[str, Any]:
        """
        CREATED_BY リレーションを生成（サービス等利用計画→相談支援専門員）
        
        Args:
            service_plan_id: サービス等利用計画ノードID
            specialist_id: 相談支援専門員ノードID
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="CREATED_BY",
            source_id=service_plan_id,
            target_id=specialist_id,
            direction="directed",
            properties={},
            layer="service_plans"
        )
        return relation
    
    def generate_works_for_relation(self, person_id: str, office_id: str, role: str = "") -> Dict[str, Any]:
        """
        WORKS_FOR リレーションを生成（専門員/医師/管理責任者→事業所/医療機関）
        
        Args:
            person_id: 専門員/医師/管理責任者のノードID
            office_id: 事業所/医療機関のノードID
            role: 役割（オプション）
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="WORKS_FOR",
            source_id=person_id,
            target_id=office_id,
            direction="directed",
            properties={"role": role} if role else {},
            layer="consultation_supports"  # レイヤーは状況により変わる
        )
        return relation
    
    def generate_contract_with_relation(self, contract_id: str, service_id: str) -> Dict[str, Any]:
        """
        CONTRACT_WITH リレーションを生成（サービス契約→福祉サービス事業所）
        
        Args:
            contract_id: サービス契約ノードID
            service_id: 福祉サービス事業所ノードID
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="CONTRACT_WITH",
            source_id=contract_id,
            target_id=service_id,
            direction="directed",
            properties={},
            layer="service_contracts"
        )
        return relation
    
    def generate_managed_by_relation(self, contract_id: str, manager_id: str) -> Dict[str, Any]:
        """
        MANAGED_BY リレーションを生成（サービス契約→サービス管理責任者）
        
        Args:
            contract_id: サービス契約ノードID
            manager_id: サービス管理責任者ノードID
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="MANAGED_BY",
            source_id=contract_id,
            target_id=manager_id,
            direction="directed",
            properties={},
            layer="service_contracts"
        )
        return relation
    
    def generate_diagnosed_by_relation(self, diagnosis_id: str, doctor_id: str) -> Dict[str, Any]:
        """
        DIAGNOSED_BY リレーションを生成（診断→医師）
        
        Args:
            diagnosis_id: 診断ノードID
            doctor_id: 医師ノードID
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="DIAGNOSED_BY",
            source_id=diagnosis_id,
            target_id=doctor_id,
            direction="directed",
            properties={},
            layer="diagnoses"
        )
        return relation
    
    def generate_renewed_from_relation(self, new_notebook_id: str, old_notebook_id: str) -> Dict[str, Any]:
        """
        RENEWED_FROM リレーションを生成（新手帳→旧手帳）履歴
        
        Args:
            new_notebook_id: 新しい手帳ノードID
            old_notebook_id: 古い手帳ノードID
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="RENEWED_FROM",
            source_id=new_notebook_id,
            target_id=old_notebook_id,
            direction="directed",
            properties={"history_type": "renewal"},
            layer="notebooks",
            line_style="dashed"
        )
        return relation
    
    def generate_changed_from_relation(self, new_level_id: str, old_level_id: str) -> Dict[str, Any]:
        """
        CHANGED_FROM リレーションを生成（新支援区分→旧支援区分）履歴
        
        Args:
            new_level_id: 新しい支援区分ノードID
            old_level_id: 古い支援区分ノードID
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="CHANGED_FROM",
            source_id=new_level_id,
            target_id=old_level_id,
            direction="directed",
            properties={"history_type": "change"},
            layer="support_levels",
            line_style="dashed"
        )
        return relation
    
    def generate_revised_from_relation(self, new_plan_id: str, old_plan_id: str) -> Dict[str, Any]:
        """
        REVISED_FROM リレーションを生成（新計画→旧計画）履歴
        
        Args:
            new_plan_id: 新しいサービス等利用計画ノードID
            old_plan_id: 古いサービス等利用計画ノードID
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="REVISED_FROM",
            source_id=new_plan_id,
            target_id=old_plan_id,
            direction="directed",
            properties={"history_type": "revision"},
            layer="service_plans",
            line_style="dashed"
        )
        return relation
    
    def generate_prescribed_by_relation(self, medication_id: str, doctor_id: str) -> Dict[str, Any]:
        """
        PRESCRIBED_BY リレーションを生成（処方薬→医師）
        
        Args:
            medication_id: 処方薬ノードID
            doctor_id: 医師ノードID
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="PRESCRIBED_BY",
            source_id=medication_id,
            target_id=doctor_id,
            direction="directed",
            properties={},
            layer="medical"
        )
        return relation
    
    def generate_takes_medication_relation(self, person_id: str, medication_id: str) -> Dict[str, Any]:
        """
        TAKES_MEDICATION リレーションを生成（本人→処方薬）
        
        Args:
            person_id: 本人ノードID
            medication_id: 処方薬ノードID
            
        Returns:
            リレーション辞書
        """
        relation = self._create_relation(
            relation_type="TAKES_MEDICATION",
            source_id=person_id,
            target_id=medication_id,
            direction="directed",
            properties={},
            layer="medical"
        )
        return relation
    
    def _create_relation(
        self,
        relation_type: str,
        source_id: str,
        target_id: str,
        direction: str,
        properties: Dict[str, Any],
        layer: str,
        line_style: str = "solid"
    ) -> Dict[str, Any]:
        """
        リレーションを作成
        
        Args:
            relation_type: リレーションタイプ
            source_id: 始点ノードID
            target_id: 終点ノードID
            direction: 方向（"directed" or "undirected"）
            properties: プロパティ
            layer: レイヤー名
            line_style: 線のスタイル（"solid" or "dashed"）
            
        Returns:
            リレーション辞書
        """
        relation_id = str(uuid.uuid4())
        
        relation = {
            "id": relation_id,
            "type": relation_type,
            "source_id": source_id,
            "target_id": target_id,
            "properties": properties,
            "direction": direction,
            "display": {
                "line_style": line_style,
                "line_width": 2,
                "color": "#999",
                "arrow": direction == "directed",
            },
            "layer": layer,
            "created_at": datetime.now().isoformat(),
        }
        
        self.generated_relations.append(relation)
        return relation


if __name__ == "__main__":
    print("=== RelationGenerator テスト ===")
    
    generator = RelationGenerator()
    
    # テスト用のノードID
    person_id = "person-123"
    notebook_id = "notebook-456"
    family_id = "family-789"
    
    # HAS_NOTEBOOK リレーション
    print("\n【HAS_NOTEBOOK リレーション】")
    relation1 = generator.generate_has_notebook_relation(person_id, notebook_id)
    print(f"ID: {relation1['id']}")
    print(f"タイプ: {relation1['type']}")
    print(f"方向: {relation1['direction']}")
    print(f"表示: {relation1['display']}")
    
    # FAMILY_RELATION リレーション
    print("\n【FAMILY_RELATION リレーション】")
    relation2 = generator.generate_family_relation(person_id, family_id, "母")
    print(f"タイプ: {relation2['type']}")
    print(f"方向: {relation2['direction']}")
    print(f"プロパティ: {relation2['properties']}")
    
    # RENEWED_FROM リレーション（履歴）
    print("\n【RENEWED_FROM リレーション（履歴）】")
    relation3 = generator.generate_renewed_from_relation("new-notebook-111", "old-notebook-222")
    print(f"タイプ: {relation3['type']}")
    print(f"線のスタイル: {relation3['display']['line_style']}")
    
    print(f"\n生成したリレーション数: {len(generator.generated_relations)}")
