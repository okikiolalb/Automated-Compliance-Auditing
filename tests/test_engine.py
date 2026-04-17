import pytest
from src.auditor.models import Room
from src.auditor.engine import ComplianceEngine

@pytest.fixture
def engine():
    return ComplianceEngine()

def test_compliant_room(engine):
    room = Room(id="1", name="Sala de Jantar", area=15.0, height=2.8)
    result = engine.audit_room(room)
    assert result.is_compliant is True
    assert len(result.failures) == 0

def test_non_compliant_height(engine):
    room = Room(id="2", name="Corredor", area=5.0, height=2.5) # Height < 2.7
    result = engine.audit_room(room)
    assert result.is_compliant is False
    assert len(result.failures) == 1
    assert result.failures[0].rule_id == "ART_65_HEIGHT"

def test_non_compliant_area(engine):
    room = Room(id="3", name="Quarto Principal", area=9.0, height=2.8) # Area < 10.5
    result = engine.audit_room(room)
    assert result.is_compliant is False
    assert len(result.failures) == 1
    assert result.failures[0].rule_id == "ART_67_AREA"

def test_multiple_failures(engine):
    room = Room(id="4", name="Cozinha", area=5.0, height=2.5) # Area < 6.0, Height < 2.7
    result = engine.audit_room(room)
    assert result.is_compliant is False
    assert len(result.failures) == 2

def test_audit_project_report(engine):
    rooms = [
        Room(id="1", name="Sala", area=15.0, height=2.8),
        Room(id="2", name="Quarto", area=9.0, height=2.8) # Failing area
    ]
    report = engine.audit_project(rooms)
    assert report.total_rooms == 2
    assert report.compliant_rooms == 1
    assert report.non_compliant_rooms == 1

def test_untracked_room_type(engine):
    # A room whose name does not match any specific area rule in RGEU_RULES
    room = Room(id="5", name="Escritorio", area=4.0, height=2.8)
    result = engine.audit_room(room)
    assert result.is_compliant is True
    
def test_case_insensitive_matching(engine):
    # Ensure matching ignores case
    room = Room(id="6", name="SALA DE ESTAR", area=10.0, height=2.8) # Sala is min 12.0
    result = engine.audit_room(room)
    assert result.is_compliant is False
    assert result.failures[0].rule_id == "ART_67_AREA"

def test_custom_rules_engine():
    # Pass custom rules to the engine
    custom_rules = {
        "min_height": 3.0,
        "min_areas": {
            "Office": 10.0
        }
    }
    custom_engine = ComplianceEngine(rules=custom_rules)
    
    room_compliant = Room(id="1", name="Office", area=12.0, height=3.1)
    res_compliant = custom_engine.audit_room(room_compliant)
    assert res_compliant.is_compliant is True
    
    room_failing = Room(id="2", name="Office", area=8.0, height=2.8)
    res_failing = custom_engine.audit_room(room_failing)
    assert res_failing.is_compliant is False
    assert len(res_failing.failures) == 2

