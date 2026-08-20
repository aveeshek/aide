import json
from datetime import date

from neo4j.time import Date, DateTime, Duration

from knowledge_plane.graph_store import json_safe, optional_str


def test_neo4j_temporal_properties_are_json_serializable() -> None:
    entity = {
        "id": "service.order",
        "updated_at": DateTime(2026, 7, 22, 10, 30, 0),
        "graphiti_synced_at": DateTime(2026, 7, 22, 10, 31, 0),
        "valid_from": Date(2026, 1, 15),
        "retention": Duration(days=30),
    }

    safe = json_safe(entity)

    assert json.loads(json.dumps(safe))["id"] == "service.order"
    assert safe["updated_at"].startswith("2026-07-22T10:30:00")
    assert safe["valid_from"] == "2026-01-15"
    # Duration subclasses tuple; it must stay an ISO string, not a flattened list.
    assert safe["retention"] == "P30D"


def test_primitives_and_containers_are_preserved() -> None:
    payload = {
        "kind": "Service",
        "status": None,
        "review_status": "approved",
        "depth": 2,
        "approved": True,
        "outgoing": [
            {"type": "EXPOSES", "target": "api.order.v2", "seen_at": DateTime(2026, 7, 22)},
        ],
    }

    safe = json_safe(payload)

    assert safe["kind"] == "Service"
    assert safe["status"] is None
    assert safe["depth"] == 2
    assert safe["approved"] is True
    assert safe["outgoing"][0]["target"] == "api.order.v2"
    assert isinstance(safe["outgoing"][0]["seen_at"], str)
    json.dumps(safe)


def test_optional_str_keeps_absent_validity_absent() -> None:
    # YAML null and blank values must not become an empty-string property, which would
    # compare as a real bound in a validity-window check.
    assert optional_str(None) is None
    assert optional_str("") is None
    assert optional_str("   ") is None


def test_optional_str_preserves_real_values() -> None:
    assert optional_str("2026-01-15") == "2026-01-15"
    assert optional_str(date(2026, 1, 15)) == "2026-01-15"
    assert optional_str("  2026-01-15  ") == "2026-01-15"
