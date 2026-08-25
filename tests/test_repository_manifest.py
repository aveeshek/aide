"""Tests for manifest resolution and the frozen-commit gate."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from knowledge_plane.repository_manifest import (
    DEFAULT_MANIFEST_RELATIVE_PATH,
    CommitMismatchError,
    GitInspectionError,
    RepositoryManifestError,
    RepositoryPathError,
    RepositoryRecord,
    UnknownRepositoryError,
    load_repository_manifest,
    read_git_head,
    resolve_repository,
    resolve_source_files,
    verify_expected_commit,
)

FROZEN_COMMIT = "52b1fd1b5d808e32b7925e890f560445a8460e7a"
OTHER_COMMIT = "0123456789abcdef0123456789abcdef01234567"
AIDE_ROOT = Path(__file__).resolve().parents[1]


def write_manifest(path: Path, repositories: list[dict]) -> Path:
    path.write_text(
        yaml.safe_dump({"version": 1, "repositories": repositories}, sort_keys=False),
        encoding="utf-8",
    )
    return path


def make_record(
    repo_root: Path, *, expected_commit: str | None = FROZEN_COMMIT
) -> RepositoryRecord:
    return RepositoryRecord(
        id="ftgo",
        path=repo_root,
        url="https://example.invalid/ftgo.git",
        default_branch="main",
        expected_commit=expected_commit,
        owner="aide-ftgo-cohort",
        sources={"compose": ("backend/docker-compose.yaml", "backend/infra/**/*.yaml")},
    )


# --------------------------------------------------------------------------------------
# The manifest actually shipped in this repository
# --------------------------------------------------------------------------------------


def test_shipped_manifest_registers_ftgo_at_the_frozen_commit() -> None:
    records = load_repository_manifest(AIDE_ROOT / DEFAULT_MANIFEST_RELATIVE_PATH)

    assert "ftgo" in records
    ftgo = records["ftgo"]
    assert ftgo.expected_commit == FROZEN_COMMIT
    assert ftgo.owner == "aide-ftgo-cohort"
    assert ftgo.source_patterns("compose") == (
        "backend/docker-compose.yaml",
        "backend/infra/**/*.yaml",
    )


# --------------------------------------------------------------------------------------
# Loading and resolution
# --------------------------------------------------------------------------------------


def test_missing_manifest_is_reported(tmp_path: Path) -> None:
    with pytest.raises(RepositoryManifestError, match="not found"):
        load_repository_manifest(tmp_path / "absent.yaml")


def test_duplicate_repository_id_is_rejected(tmp_path: Path) -> None:
    manifest = write_manifest(
        tmp_path / "repositories.yaml",
        [{"id": "ftgo", "path": str(tmp_path)}, {"id": "ftgo", "path": str(tmp_path)}],
    )

    with pytest.raises(RepositoryManifestError, match="duplicate repository id"):
        load_repository_manifest(manifest)


def test_repository_entry_requires_a_path(tmp_path: Path) -> None:
    manifest = write_manifest(tmp_path / "repositories.yaml", [{"id": "ftgo"}])

    with pytest.raises(RepositoryManifestError, match="requires a path"):
        load_repository_manifest(manifest)


def test_unknown_repository_id_lists_registered_ids(tmp_path: Path) -> None:
    manifest = write_manifest(
        tmp_path / "repositories.yaml", [{"id": "ftgo", "path": str(tmp_path)}]
    )

    with pytest.raises(UnknownRepositoryError) as excinfo:
        resolve_repository("nope", manifest)

    assert "ftgo" in str(excinfo.value)


def test_missing_repository_path_is_reported(tmp_path: Path) -> None:
    manifest = write_manifest(
        tmp_path / "repositories.yaml",
        [{"id": "ftgo", "path": str(tmp_path / "absent")}],
    )

    with pytest.raises(RepositoryPathError):
        resolve_repository("ftgo", manifest)


# --------------------------------------------------------------------------------------
# Commit gating
# --------------------------------------------------------------------------------------


def test_matching_commit_is_accepted(tmp_path: Path) -> None:
    record = make_record(tmp_path)

    assert verify_expected_commit(record, FROZEN_COMMIT) == FROZEN_COMMIT
    # Case differences in the recorded SHA must not fail the gate.
    assert verify_expected_commit(record, FROZEN_COMMIT.upper()) == FROZEN_COMMIT


def test_commit_mismatch_aborts_with_both_commits(tmp_path: Path) -> None:
    record = make_record(tmp_path)

    with pytest.raises(CommitMismatchError) as excinfo:
        verify_expected_commit(record, OTHER_COMMIT)

    error = excinfo.value
    assert error.expected == FROZEN_COMMIT
    assert error.actual == OTHER_COMMIT
    assert "Extraction aborted" in str(error)


def test_missing_expected_commit_is_refused(tmp_path: Path) -> None:
    record = make_record(tmp_path, expected_commit=None)

    with pytest.raises(RepositoryManifestError, match="no expected_commit"):
        verify_expected_commit(record, FROZEN_COMMIT)


def test_read_git_head_returns_a_full_sha_for_a_real_repository() -> None:
    head = read_git_head(AIDE_ROOT)

    assert len(head) == 40
    assert head == head.lower()
    assert all(character in "0123456789abcdef" for character in head)


def test_read_git_head_fails_outside_a_repository(tmp_path: Path) -> None:
    with pytest.raises(GitInspectionError):
        read_git_head(tmp_path / "not-a-repo-at-all")


# --------------------------------------------------------------------------------------
# Source pattern expansion
# --------------------------------------------------------------------------------------


def test_source_files_are_sorted_deduplicated_and_relative(tmp_path: Path) -> None:
    (tmp_path / "backend/infra/redis").mkdir(parents=True)
    (tmp_path / "backend/docker-compose.yaml").write_text("services: {}", encoding="utf-8")
    (tmp_path / "backend/infra/redis/docker-compose.yaml").write_text(
        "services: {}", encoding="utf-8"
    )
    # Overlapping patterns must not produce duplicates.
    record = RepositoryRecord(
        id="ftgo",
        path=tmp_path,
        url=None,
        default_branch=None,
        expected_commit=FROZEN_COMMIT,
        owner=None,
        sources={
            "compose": (
                "backend/infra/**/*.yaml",
                "backend/docker-compose.yaml",
                "backend/infra/redis/docker-compose.yaml",
            )
        },
    )

    assert resolve_source_files(record, "compose") == (
        "backend/docker-compose.yaml",
        "backend/infra/redis/docker-compose.yaml",
    )


def test_absent_files_are_skipped_not_invented(tmp_path: Path) -> None:
    (tmp_path / "backend").mkdir()
    record = make_record(tmp_path)

    assert resolve_source_files(record, "compose") == ()


def test_unknown_source_kind_is_reported(tmp_path: Path) -> None:
    record = make_record(tmp_path)

    with pytest.raises(RepositoryManifestError, match="declares no 'code' sources"):
        resolve_source_files(record, "code")


def test_patterns_may_not_escape_the_repository_root(tmp_path: Path) -> None:
    record = RepositoryRecord(
        id="ftgo",
        path=tmp_path,
        url=None,
        default_branch=None,
        expected_commit=FROZEN_COMMIT,
        owner=None,
        sources={"compose": ("../outside/docker-compose.yaml",)},
    )

    with pytest.raises(RepositoryManifestError, match="unsafe"):
        resolve_source_files(record, "compose")
