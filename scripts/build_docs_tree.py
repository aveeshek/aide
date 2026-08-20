#!/usr/bin/env python3
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / ".site-docs"


def copy_tree(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    if source.exists():
        shutil.copytree(source, destination, dirs_exist_ok=True)


def main() -> None:
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    copy_tree(ROOT / "wiki", DEST / "approved")
    copy_tree(ROOT / "openwiki", DEST / "generated")
    p = DEST / "generated" / "INSTRUCTIONS.md"
    if p.exists():
        p.unlink()
    copy_tree(ROOT / "operations", DEST / "operations")
    copy_tree(ROOT / "enterprise-specs", DEST / "enterprise-specs")
    copy_tree(ROOT / "docs", DEST / "architecture")
    for p in (DEST / "architecture").glob("*.docx"):
        p.unlink()
    (DEST / "index.md").write_text(
        "# BOS AIDE Knowledge-Centric Loop Engineering\n\n"
        "- **Approved Knowledge** is canonical after PR approval.\n"
        "- **Generated Documentation** is OpenWiki synthesis and lower trust.\n"
        "- **Architecture and Installation** describe the operating design.\n"
        "- **Knowledge Operations** expose contradictions and staleness.\n",
        encoding="utf-8",
    )
    print(f"Prepared Zensical source tree at {DEST}")


if __name__ == "__main__":
    main()
