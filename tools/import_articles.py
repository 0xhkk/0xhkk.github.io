#!/usr/bin/env python3
from __future__ import annotations

import datetime as _dt
from pathlib import Path


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _strip_leading_separator_md(text: str) -> str:
    """
    Some notes start with a standalone '---' separator (not YAML front matter).
    In Jekyll posts, we must reserve the very first '---' block for front matter.
    This function removes a single leading separator if it appears before any
    meaningful content.
    """
    lines = text.splitlines()
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i < len(lines) and lines[i].strip() == "---":
        # Drop this line and a single following blank line (if any).
        i += 1
        if i < len(lines) and lines[i].strip() == "":
            i += 1
        return "\n".join(lines[i:]).lstrip("\n") + ("\n" if text.endswith("\n") else "")
    return text


def _write_post(out_dir: Path, date: str, slug: str, title: str, body_md: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{date}-{slug}.md"
    front_matter = "\n".join(
        [
            "---",
            "layout: post",
            f'title: "{title}"',
            "---",
            "",
        ]
    )
    out_path.write_text(front_matter + body_md, encoding="utf-8")
    return out_path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    source_root = repo_root.parent  # your current notes folder

    # Map: (source filename, slug, title)
    articles = [
        ("1.spl-token-简明指南.md", "spl-token", "一文搞懂 SPL Token"),
        ("3.pda-deep-dive.md", "pda-deep-dive", "PDA 深度解析 —— 程序没有私钥，怎么控制账户？"),
    ]

    date = _dt.date.today().strftime("%Y-%m-%d")
    out_dir = repo_root / "_posts"

    written = []
    for filename, slug, title in articles:
        src = source_root / filename
        if not src.exists():
            raise FileNotFoundError(f"Missing source markdown: {src}")
        body = _read_text(src)
        body = _strip_leading_separator_md(body)
        written.append(_write_post(out_dir, date, slug, title, body))

    print("Generated posts:")
    for p in written:
        print(f"- {p.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


