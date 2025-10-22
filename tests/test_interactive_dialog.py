#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
対話エンジンモジュールのテスト
"""

import pytest
import sys
from pathlib import Path

# パスを追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.interactive_dialog import InteractiveDialogEngine, DialogState


def test_start_session():
    """セッション開始"""
    engine = InteractiveDialogEngine()
    message = engine.start_session("田中一郎")

    assert "田中一郎" in message
    assert engine.state == DialogState.COLLECT_PERSON
    assert engine.collected_data["person"]["name"] == "田中一郎"


def test_process_person_info():
    """本人情報収集"""
    engine = InteractiveDialogEngine()
    engine.start_session()

    # 氏名
    response = engine.process_input("田中一郎")
    assert "田中一郎" in response

    # 生年月日
    response = engine.process_input("2000-04-15")
    assert "歳" in response

    # 性別
    response = engine.process_input("男")
    assert "家族" in response
    assert engine.state == DialogState.COLLECT_FAMILY


def test_skip_family():
    """家族情報のスキップ"""
    engine = InteractiveDialogEngine()
    engine.state = DialogState.COLLECT_FAMILY
    engine.step_count = 2

    response = engine.process_input("なし")
    assert "手帳" in response
    assert engine.state == DialogState.COLLECT_NOTEBOOK


def test_notebook_collection():
    """手帳情報収集"""
    engine = InteractiveDialogEngine()
    engine.state = DialogState.COLLECT_NOTEBOOK
    engine.step_count = 3

    # 手帳種別
    response = engine.process_input("療育手帳")
    assert "等級" in response

    # 等級
    response = engine.process_input("A1")
    assert "交付日" in response

    # 交付日
    response = engine.process_input("2020-04-01")
    assert "有効期限" in response

    # 有効期限
    response = engine.process_input("2025-03-31")
    assert len(engine.collected_data["notebooks"]) == 1
    assert engine.collected_data["notebooks"][0]["type"] == "療育手帳"


def test_is_complete():
    """完了判定"""
    engine = InteractiveDialogEngine()
    assert not engine.is_complete()

    engine.state = DialogState.COMPLETE
    assert engine.is_complete()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
