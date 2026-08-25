from pathlib import Path

from knowledge_plane.markdown_loader import load_pages, validate_pages
from knowledge_plane.ontology import load_entity_types, load_relationship_types

ROOT = Path(__file__).resolve().parents[1]


def test_canonical_knowledge_is_valid() -> None:
    pages = load_pages(ROOT / "wiki", ROOT)
    kinds = load_entity_types(ROOT / "ontology/entity-types.yaml")
    relations = load_relationship_types(ROOT / "ontology/relationship-types.yaml")

    assert not validate_pages(pages, kinds, relations)

    page_ids = {page.id for page in pages}

    assert {
        "knowledge.ftgo",
        "service.ftgo.gateway",
        "service.ftgo.user",
        "service.ftgo.restaurant",
        "service.ftgo.location",
        "service.ftgo.order",
        "service.ftgo.feedback",
        "component.ftgo.rabbitmq",
        "database.ftgo.order-mongo",
    } <= page_ids