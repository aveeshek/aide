"""Deterministic resolution of registered source repositories.

Graph Engineering extraction reads foreign repositories that this repository does not
own. Every extraction is therefore pinned to a manifest entry and a frozen commit: the
manifest declares where a repository lives and which commit its evidence was approved
against, and extraction aborts when the working tree has moved. Nothing here writes to a
registered repository; the only git command used is a read-only rev-parse.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

DEFAULT_MANIFEST_RELATIVE_PATH = Path("manifests/repositories.yaml")
_COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
_GLOB_CHARACTERS = ("*", "?", "[")
# Reading a registered repository must never escape its declared root.
_FORBIDDEN_PATTERN_SEGMENT = ".."


class RepositoryManifestError(RuntimeError):
    """Base class for manifest resolution and commit-gating failures."""


class UnknownRepositoryError(RepositoryManifestError):
    """Raised when a repository id is not registered in the manifest."""


class RepositoryPathError(RepositoryManifestError):
    """Raised when a registered repository path is missing or is not a directory."""


class GitInspectionError(RepositoryManifestError):
    """Raised when the HEAD commit of a registered repository cannot be read."""


class CommitMismatchError(RepositoryManifestError):
    """Raised when repository HEAD does not equal the manifest's expected commit."""

    def __init__(self, repository_id: str, expected: str, actual: str) -> None:
        self.repository_id = repository_id
        self.expected = expected
        self.actual = actual
        super().__init__(
            f"Repository {repository_id!r} is at commit {actual} but the manifest expects "
            f"{expected}. Extraction aborted: candidate evidence must be provably tied to "
            f"the frozen baseline. Check out the expected commit or update the manifest "
            f"through review."
        )


@dataclass(frozen=True, slots=True)
class RepositoryRecord:
    """One registered repository, as declared in the manifest."""

    id: str
    path: Path
    url: str | None
    default_branch: str | None
    expected_commit: str | None
    owner: str | None
    sources: dict[str, tuple[str, ...]]

    def source_patterns(self, kind: str) -> tuple[str, ...]:
        return self.sources.get(kind, ())


def _coerce_patterns(raw: Any) -> tuple[str, ...]:
    if raw in (None, ""):
        return ()
    if isinstance(raw, str):
        return (raw,)
    if isinstance(raw, list):
        return tuple(str(item).strip() for item in raw if str(item).strip())
    raise RepositoryManifestError("Source patterns must be a string or a list of strings")


def _optional_text(raw: Any) -> str | None:
    if raw is None:
        return None
    text = str(raw).strip()
    return text or None


def load_repository_manifest(manifest_path: Path) -> dict[str, RepositoryRecord]:
    """Parse the repository manifest into records keyed by repository id."""
    if not manifest_path.is_file():
        raise RepositoryManifestError(f"Repository manifest not found: {manifest_path}")

    document = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    if not isinstance(document, dict):
        raise RepositoryManifestError(f"{manifest_path}: manifest must be a mapping")

    entries = document.get("repositories") or []
    if not isinstance(entries, list):
        raise RepositoryManifestError(f"{manifest_path}: 'repositories' must be a list")

    records: dict[str, RepositoryRecord] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise RepositoryManifestError(
                f"{manifest_path}: repositories[{index}] must be a mapping"
            )
        repository_id = _optional_text(entry.get("id"))
        if not repository_id:
            raise RepositoryManifestError(
                f"{manifest_path}: repositories[{index}] requires a non-empty id"
            )
        if repository_id in records:
            raise RepositoryManifestError(
                f"{manifest_path}: duplicate repository id {repository_id!r}"
            )

        raw_path = _optional_text(entry.get("path"))
        if not raw_path:
            raise RepositoryManifestError(
                f"{manifest_path}: repository {repository_id!r} requires a path"
            )

        raw_sources = entry.get("sources") or {}
        if not isinstance(raw_sources, dict):
            raise RepositoryManifestError(
                f"{manifest_path}: repository {repository_id!r} sources must be a mapping"
            )

        records[repository_id] = RepositoryRecord(
            id=repository_id,
            path=Path(raw_path).expanduser(),
            url=_optional_text(entry.get("url")),
            default_branch=_optional_text(entry.get("default_branch")),
            expected_commit=_optional_text(entry.get("expected_commit")),
            owner=_optional_text(entry.get("owner")),
            sources={
                str(kind): _coerce_patterns(patterns) for kind, patterns in raw_sources.items()
            },
        )
    return records


def resolve_repository(
    repository_id: str,
    manifest_path: Path,
    *,
    require_existing_path: bool = True,
) -> RepositoryRecord:
    """Look up one repository and confirm its declared path is usable."""
    records = load_repository_manifest(manifest_path)
    record = records.get(repository_id)
    if record is None:
        known = ", ".join(sorted(records)) or "<none>"
        raise UnknownRepositoryError(
            f"Repository id {repository_id!r} is not registered in {manifest_path}. "
            f"Registered ids: {known}."
        )
    if require_existing_path and not record.path.is_dir():
        raise RepositoryPathError(
            f"Repository {repository_id!r} is registered at {record.path}, which does not "
            f"exist or is not a directory."
        )
    return record


def read_git_head(repository_path: Path) -> str:
    """Return the HEAD commit of ``repository_path``. Read-only; never mutates the tree."""
    try:
        completed = subprocess.run(  # noqa: S603 - fixed argv, no shell interpolation
            ["git", "-C", str(repository_path), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        raise GitInspectionError(
            f"Unable to run git for {repository_path}: {exc}. git must be on PATH to verify "
            f"the extraction baseline."
        ) from exc

    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "").strip()
        raise GitInspectionError(
            f"git rev-parse HEAD failed for {repository_path} "
            f"(exit {completed.returncode}): {detail}"
        )

    commit = completed.stdout.strip().lower()
    if not _COMMIT_PATTERN.match(commit):
        raise GitInspectionError(
            f"git rev-parse HEAD returned {commit!r} for {repository_path}, which is not a "
            f"40-character hexadecimal commit id."
        )
    return commit


def verify_expected_commit(record: RepositoryRecord, actual_commit: str) -> str:
    """Gate extraction on the frozen baseline, returning the verified commit."""
    expected = (record.expected_commit or "").strip().lower()
    actual = actual_commit.strip().lower()
    if not expected:
        raise RepositoryManifestError(
            f"Repository {record.id!r} has no expected_commit in the manifest. Extraction "
            f"requires a frozen baseline commit."
        )
    if expected != actual:
        raise CommitMismatchError(record.id, expected, actual)
    return actual


def resolve_source_files(record: RepositoryRecord, kind: str) -> tuple[str, ...]:
    """Expand the manifest source patterns for ``kind`` into repository-relative paths.

    Results are sorted and de-duplicated so the same repository state always yields the
    same file list, and paths are POSIX-relative so extraction output never embeds an
    absolute workstation path.
    """
    patterns = record.source_patterns(kind)
    if not patterns:
        raise RepositoryManifestError(
            f"Repository {record.id!r} declares no {kind!r} sources in the manifest."
        )

    matches: set[str] = set()
    for pattern in patterns:
        normalized = pattern.replace("\\", "/").strip()
        if not normalized:
            continue
        if _FORBIDDEN_PATTERN_SEGMENT in normalized.split("/"):
            raise RepositoryManifestError(
                f"Repository {record.id!r} has an unsafe {kind!r} source pattern "
                f"{pattern!r}: patterns must stay inside the repository root."
            )
        if any(character in normalized for character in _GLOB_CHARACTERS):
            candidates = record.path.glob(normalized)
        else:
            candidates = iter([record.path / normalized])
        for candidate in candidates:
            if candidate.is_file():
                matches.add(candidate.relative_to(record.path).as_posix())
    return tuple(sorted(matches))
