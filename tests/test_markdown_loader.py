from pathlib import Path

from knowledge_plane.markdown_loader import load_pages, validate_pages
from knowledge_plane.ontology import load_entity_types, load_relationship_types

ROOT = Path(__file__).resolve().parents[1]


def test_sample_knowledge_is_valid() -> None:
    pages = load_pages(ROOT / "wiki", ROOT)
    kinds = load_entity_types(ROOT / "ontology/entity-types.yaml")
    relations = load_relationship_types(ROOT / "ontology/relationship-types.yaml")
    assert not validate_pages(pages, kinds, relations)
    assert {page.id for page in pages} >= {
        "service.order",
        "service.payment",
        "api.order.v2",
        "flow.place-order",
    }
