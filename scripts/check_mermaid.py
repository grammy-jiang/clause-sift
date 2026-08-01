#!/usr/bin/env python3
"""Validate Mermaid code fences embedded in Markdown files.

The checker extracts every fenced code block whose info string starts with
``mermaid`` and asks the official Mermaid CLI to parse and render it. Rendering
is intentional: it catches parser and configuration failures that a lightweight
regular-expression check would miss.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

MERMAID_CLI_VERSION = "11.15.0"
FENCE_PATTERN = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})(.*)$")


@dataclass(frozen=True, slots=True)
class MermaidBlock:
    """One Mermaid diagram extracted from a Markdown file."""

    path: Path
    start_line: int
    content: str


def extract_mermaid_blocks(path: Path) -> tuple[list[MermaidBlock], list[str]]:
    """Extract Mermaid fences and report malformed Mermaid fence boundaries."""

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    blocks: list[MermaidBlock] = []
    errors: list[str] = []

    fence_char: str | None = None
    fence_length = 0
    is_mermaid = False
    start_line = 0
    content_lines: list[str] = []

    for line_number, line in enumerate(lines, start=1):
        match = FENCE_PATTERN.match(line)

        if fence_char is None:
            if match is None:
                continue

            marker, info = match.groups()
            fence_char = marker[0]
            fence_length = len(marker)
            first_info_token = info.strip().split(maxsplit=1)[0].lower() if info.strip() else ""
            is_mermaid = first_info_token == "mermaid"
            start_line = line_number
            content_lines = []
            continue

        closing_pattern = rf"^[ \t]{{0,3}}{re.escape(fence_char)}{{{fence_length},}}[ \t]*$"
        if re.match(closing_pattern, line):
            if is_mermaid:
                content = "\n".join(content_lines).strip()
                if content:
                    blocks.append(MermaidBlock(path=path, start_line=start_line, content=content))
                else:
                    errors.append(f"{path}:{start_line}: empty Mermaid diagram")

            fence_char = None
            fence_length = 0
            is_mermaid = False
            start_line = 0
            content_lines = []
            continue

        if is_mermaid:
            content_lines.append(line)

    if fence_char is not None and is_mermaid:
        errors.append(f"{path}:{start_line}: unclosed Mermaid code fence")

    return blocks, errors


def mermaid_command() -> list[str]:
    """Return the Mermaid CLI command, preferring an installed ``mmdc``."""

    override = os.environ.get("MERMAID_CLI")
    if override:
        executable = shutil.which(override)
        if executable is None:
            raise RuntimeError(f"MERMAID_CLI points to an unavailable executable: {override}")
        return [executable]

    installed = shutil.which("mmdc")
    if installed is not None:
        return [installed]

    npx = shutil.which("npx")
    if npx is None:
        raise RuntimeError(
            "Mermaid CLI is unavailable. Install Node.js with npx, or install "
            "@mermaid-js/mermaid-cli and expose mmdc on PATH."
        )

    return [
        npx,
        "--yes",
        "--package",
        f"@mermaid-js/mermaid-cli@{MERMAID_CLI_VERSION}",
        "mmdc",
    ]


def validate_block(block: MermaidBlock, command: Sequence[str]) -> str | None:
    """Render one block and return an error message when validation fails."""

    with tempfile.TemporaryDirectory(prefix="clausesift-mermaid-") as directory:
        temp_dir = Path(directory)
        input_path = temp_dir / "diagram.mmd"
        output_path = temp_dir / "diagram.svg"
        puppeteer_config = temp_dir / "puppeteer-config.json"

        input_path.write_text(f"{block.content}\n", encoding="utf-8")
        puppeteer_config.write_text(
            '{"args":["--no-sandbox","--disable-setuid-sandbox"]}\n',
            encoding="utf-8",
        )

        process = subprocess.run(
            [
                *command,
                "--input",
                str(input_path),
                "--output",
                str(output_path),
                "--puppeteerConfigFile",
                str(puppeteer_config),
                "--quiet",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        if process.returncode == 0 and output_path.exists():
            return None

        details = "\n".join(
            part.strip() for part in (process.stdout, process.stderr) if part.strip()
        )
        if not details:
            details = f"Mermaid CLI exited with status {process.returncode}."

        return f"{block.path}:{block.start_line}: Mermaid validation failed\n{details}"


def markdown_paths(arguments: Iterable[str]) -> list[Path]:
    """Return existing Markdown paths, preserving deterministic order."""

    paths = {
        Path(argument)
        for argument in arguments
        if Path(argument).is_file() and Path(argument).suffix.lower() in {".md", ".markdown"}
    }
    return sorted(paths, key=lambda path: path.as_posix())


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Mermaid fenced diagrams in Markdown files."
    )
    parser.add_argument("files", nargs="*", help="Markdown files to inspect")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    paths = markdown_paths(args.files)

    all_blocks: list[MermaidBlock] = []
    errors: list[str] = []

    for path in paths:
        blocks, extraction_errors = extract_mermaid_blocks(path)
        all_blocks.extend(blocks)
        errors.extend(extraction_errors)

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    if not all_blocks:
        return 0

    try:
        command = mermaid_command()
    except RuntimeError as error:
        print(f"mermaid-check: {error}", file=sys.stderr)
        return 2

    for block in all_blocks:
        validation_error = validate_block(block, command)
        if validation_error is not None:
            errors.append(validation_error)

    if errors:
        print("\n\n".join(errors), file=sys.stderr)
        return 1

    print(f"Validated {len(all_blocks)} Mermaid diagram(s) in {len(paths)} Markdown file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
