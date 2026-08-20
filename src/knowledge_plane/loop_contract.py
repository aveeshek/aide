from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, field_validator


class LoopBudgets(BaseModel):
    max_iterations: int = Field(ge=1, le=20)
    max_minutes: int = Field(ge=1, le=1440)
    max_scope_expansions: int = Field(default=0, ge=0, le=5)


class VerificationGate(BaseModel):
    id: str
    description: str
    command_windows: str | None = None
    required: bool = True


class LoopContract(BaseModel):
    id: str
    kind: str
    goal: str
    allowed_repositories: list[str] = Field(min_length=1)
    allowed_paths: list[str] = Field(min_length=1)
    forbidden_actions: list[str] = Field(min_length=1)
    escalation_conditions: list[str] = Field(min_length=1)
    verification: list[VerificationGate] = Field(min_length=1)
    budgets: LoopBudgets
    terminal_states: list[str]

    @field_validator("terminal_states")
    @classmethod
    def validate_terminal_states(cls, value: list[str]) -> list[str]:
        required = {"PASS", "ESCALATE", "FAIL"}
        if set(value) != required or len(value) != 3:
            raise ValueError("terminal_states must contain exactly PASS, ESCALATE, and FAIL")
        return value


def load_contract(path: Path) -> LoopContract:
    data: dict[str, Any] = yaml.safe_load(path.read_text(encoding="utf-8"))
    return LoopContract.model_validate(data)


def write_run_manifest(contract: LoopContract, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "contract": contract.model_dump(),
        "state": "READY",
        "iteration": 0,
        "evidence": [],
        "note": (
            "Kiro implements within scope; deterministic gates prove the result; "
            "only PASS, ESCALATE, or FAIL closes the loop."
        ),
    }
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a bounded loop contract")
    parser.add_argument("contract", type=Path)
    parser.add_argument("--write-run-manifest", type=Path)
    args = parser.parse_args()
    contract = load_contract(args.contract)
    print(f"Valid loop contract: {contract.id} ({contract.kind})")
    if args.write_run_manifest:
        write_run_manifest(contract, args.write_run_manifest)
        print(f"Created run manifest: {args.write_run_manifest}")


if __name__ == "__main__":
    main()
