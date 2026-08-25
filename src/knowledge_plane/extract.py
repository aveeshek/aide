"""CLI for deterministic Graph Engineering extraction (Pass 1).

    python -m knowledge_plane.extract --repo-id ftgo --kind compose --dry-run
    python -m knowledge_plane.extract --repo-id ftgo --kind compose \
        --output-dir generated/candidates/ftgo/compose

The command resolves the repository from the manifest, verifies HEAD against the frozen
expected commit, and aborts before extraction on mismatch. It writes candidates only.
Neo4j, Graphiti, wiki/, and the source repository are never touched.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

from .extractors import AVAILABLE_KINDS, COMPOSE_KIND
from .extractors.compose import (
    ComposeExtraction,
    render_bundle,
    render_report_json,
)
from .extractors.compose import (
    extract_compose as _extract_compose,
)
from .repository_manifest import (
    DEFAULT_MANIFEST_RELATIVE_PATH,
    RepositoryManifestError,
    RepositoryRecord,
    read_git_head,
    resolve_repository,
    verify_expected_commit,
)
from .settings import settings

logger = logging.getLogger(__name__)

REPORT_FILENAME = "extraction-report.json"
CANDIDATE_SUBDIRECTORIES = ("services", "infrastructure")
EXIT_OK = 0
EXIT_ABORTED = 2


def _extract(kind: str, record: RepositoryRecord, commit: str) -> ComposeExtraction:
    if kind == COMPOSE_KIND:
        return _extract_compose(record, commit)
    raise RepositoryManifestError(
        f"Unsupported extractor kind {kind!r}. Available: {', '.join(AVAILABLE_KINDS)}."
    )


def _write_text(path: Path, content: str) -> None:
    """Write UTF-8 with LF endings so repeated runs are byte-identical on any platform."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def _prune_stale_candidates(output_dir: Path, keep: set[Path]) -> list[str]:
    """Remove candidate Markdown this run did not produce, bounded to the two subdirs.

    Without this, a renamed entity would leave an orphan candidate behind and the output
    tree would stop being a faithful picture of the current commit.
    """
    removed: list[str] = []
    for subdirectory in CANDIDATE_SUBDIRECTORIES:
        directory = output_dir / subdirectory
        if not directory.is_dir():
            continue
        for existing in sorted(directory.glob("*.md")):
            if existing.resolve() not in keep:
                existing.unlink()
                removed.append(existing.relative_to(output_dir).as_posix())
    return removed


def write_candidates(
    extraction: ComposeExtraction, output_dir: Path
) -> tuple[dict[str, Any], list[str]]:
    """Render and persist candidates plus the extraction report."""
    rendered, report = render_bundle(extraction)

    written: set[Path] = set()
    for relative_path, content in sorted(rendered.items()):
        target = output_dir / relative_path
        _write_text(target, content)
        written.add(target.resolve())

    removed = _prune_stale_candidates(output_dir, written)
    if removed:
        report = dict(report)
        report["pruned_stale_candidates"] = removed

    _write_text(output_dir / REPORT_FILENAME, render_report_json(report))
    return report, sorted(relative for relative in rendered)


def _summary_payload(
    extraction: ComposeExtraction, report: dict[str, Any], *, dry_run: bool
) -> dict[str, Any]:
    return {
        "status": "dry-run" if dry_run else "ok",
        "dry_run": dry_run,
        "extractor": report["extractor"],
        "repository": extraction.repository,
        "commit": extraction.commit,
        "commit_verified": True,
        "source_files": list(extraction.source_files),
        "counts": report["counts"],
        "application_services": [entity.id for entity in extraction.services],
        "infrastructure_entities": [entity.id for entity in extraction.infrastructure],
        "relationships": [
            f"{relation.source} -{relation.type}-> {relation.target}"
            f" ({relation.config_key}={relation.referenced_host})"
            for relation in extraction.relationships
        ],
        "unresolved_dependencies": [item.summary() for item in extraction.unresolved_dependencies],
        "warnings": list(extraction.warnings),
        "secret_values_emitted": report["secret_values_emitted"],
        "graph_mutations": 0,
        "graphiti": "disabled",
    }


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

    record = resolve_repository(repository_id, manifest_path)
    head = read_git_head(record.path)
    commit = verify_expected_commit(record, head)
    extraction = _extract(kind, record, commit)

    if dry_run:
        # Render in memory to report exactly what a real run would produce, then discard.
        _, report = render_bundle(extraction)
        return _summary_payload(extraction, report, dry_run=True)

    assert output_dir is not None  # guarded above
    report, _ = write_candidates(extraction, output_dir)
    summary = _summary_payload(extraction, report, dry_run=False)
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
