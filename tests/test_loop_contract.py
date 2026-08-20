from pathlib import Path

from knowledge_plane.loop_contract import load_contract

ROOT = Path(__file__).resolve().parents[1]


def test_reference_loop_contracts_are_valid() -> None:
    for path in sorted((ROOT / "loops").glob("*.yaml")):
        contract = load_contract(path)
        assert set(contract.terminal_states) == {"PASS", "ESCALATE", "FAIL"}
        assert contract.verification
