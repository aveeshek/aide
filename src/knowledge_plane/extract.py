"""CLI for deterministic Graph Engineering extraction.

    python -m knowledge_plane.extract --repo-id ftgo --kind compose --dry-run
    python -m knowledge_plane.extract --repo-id ftgo --kind compose \
        --output-dir generated/candidates/ftgo/compose

    python -m knowledge_plane.extract --repo-id ftgo --kind fastapi --dry-run
    python -m knowledge_plane.extract --repo-id ftgo --kind fastapi \
        --output-dir generated/candidates/ftgo/fastapi

The command resolves the repository from the manifest, verifies HEAD against the frozen
expected commit, and aborts before extraction on mismatch. It writes candidates only.
Neo4j, Graphiti, wiki/, and the source repository are never touched.

The CLI is extractor-agnostic: each kind is registered in ``extractors.EXTRACTORS`` with its
own extract, render, summarize, and owned output subdirectories.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

from .extractors import AVAILABLE_KINDS, COMPOSE_KIND, EXTRACTORS, ExtractorSpec
from .repository_manifest import (
    DEFAULT_MANIFEST_RELATIVE_PATH,
    RepositoryManifestError,
    read_git_head,
    resolve_repository,
    verify_expected_commit,
)
from .settings import settings

logger = logging.getLogger(__name__)

REPORT_FILENAME = "extraction-report.json"
EXIT_OK = 0
EXIT_ABORTED = 2


def _resolve_extractor(kind: str) -> ExtractorSpec:
    spec = EXTRACTORS.get(kind)
    if spec is None:
        raise RepositoryManifestError(
            f"Unsupported extractor kind {kind!r}. Available: {', '.join(AVAILABLE_KINDS)}."
        )
    return spec


def _write_text(path: Path, content: str) -> None:
    """Write UTF-8 with LF endings so repeated runs are byte-identical on any platform."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def _prune_stale_candidates(
    output_dir: Path, keep: set[Path], subdirectories: tuple[str, ...]
) -> list[str]:
    """Remove candidate Markdown this run did not produce, bounded to the owned subdirs.

    Without this, a renamed entity would leave an orphan candidate behind and the output
    tree would stop being a faithful picture of the current commit.
    """
    removed: list[str] = []
    for subdirectory in subdirectories:
        directory = output_dir / subdirectory
        if not directory.is_dir():
            continue
        for existing in sorted(directory.glob("*.md")):
            if existing.resolve() not in keep:
                existing.unlink()
                removed.append(existing.relative_to(output_dir).as_posix())
    return removed


def write_candidates(
    spec: ExtractorSpec, extraction: Any, output_dir: Path
) -> tuple[dict[str, Any], list[str]]:
    """Render and persist candidates plus the extraction report."""
    rendered, report = spec.render_bundle(extraction)

    written: set[Path] = set()
    for relative_path, content in sorted(rendered.items()):
        target = output_dir / relative_path
        _write_text(target, content)
        written.add(target.resolve())

    removed = _prune_stale_candidates(output_dir, written, spec.candidate_subdirectories)
    if removed:
        report = dict(report)
        report["pruned_stale_candidates"] = removed

    report_json = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    _write_text(output_dir / REPORT_FILENAME, report_json)
    return report, sorted(relative for relative in rendered)


def run(
    repository_id: str,
    kind: str,
    *,
    manifest_path: Path,
    output_dir: Path | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Resolve, verify, extract, and (unless dry-run) write candidates."""
    if not dry_run and output_dir is None:
        raise RepositoryManifestError(
            "--output-dir is required unless --dry-run is set: a real run must have a "
            "candidate destination."
        )

    spec = _resolve_extractor(kind)
    record = resolve_repository(repository_id, manifest_path)
    head = read_git_head(record.path)
    commit = verify_expected_commit(record, head)
    extraction = spec.extract(record, commit)

    if dry_run:
        # Render in memory to report exactly what a real run would produce, then discard.
        _, report = spec.render_bundle(extraction)
        summary = spec.summarize(extraction, report)
        return {"status": "dry-run", "dry_run": True, **summary}

    assert output_dir is not None  # guarded above
    report, _ = write_candidates(spec, extraction, output_dir)
    summary = {"status": "ok", "dry_run": False, **spec.summarize(extraction, report)}
    summary["output_dir"] = output_dir.as_posix()
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m knowledge_plane.extract",
        description=(
            "Deterministically extract candidate knowledge from a registered repository. "
            "Writes candidates only; never canonical knowledge, Neo4j, or Graphiti."
        ),
    )
    parser.add_argument("--repo-id", required=True, help="Repository id from the manifest")
    parser.add_argument(
        "--kind",
        default=COMPOSE_KIND,
        choices=list(AVAILABLE_KINDS),
        help="Extractor to run",
    )
    parser.add_argument(
        "--manifest",
        default=None,
        help=f"Repository manifest path (default: {DEFAULT_MANIFEST_RELATIVE_PATH.as_posix()})",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory for generated candidates. Required unless --dry-run is set.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse, verify the commit, and print the summary without writing anything",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )

    manifest_path = (
        Path(args.manifest)
        if args.manifest
        else settings.knowledge_root / DEFAULT_MANIFEST_RELATIVE_PATH
    )
    output_dir = Path(args.output_dir) if args.output_dir else None

    try:
        summary = run(
            args.repo_id,
            args.kind,
            manifest_path=manifest_path,
            output_dir=output_dir,
            dry_run=args.dry_run,
        )
    except RepositoryManifestError as exc:
        print(
            json.dumps(
                {
                    "status": "aborted",
                    "repository": args.repo_id,
                    "kind": args.kind,
                    "reason": str(exc),
                    "graph_mutations": 0,
                },
                indent=2,
            )
        )
        return EXIT_ABORTED

    print(json.dumps(summary, indent=2))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
