"""Command-line interface for repo2prompt."""

from __future__ import annotations

import argparse
import contextlib
import json
import sys
from pathlib import Path

from . import __version__
from .i18n import set_lang, t
from .packer import DEFAULT_MAX_TOKENS, pack


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="repo2prompt",
        description="Pack a repository into clean, AI-friendly context "
        "(directory tree + file contents + token stats).",
    )
    p.add_argument("path", nargs="?", default=".", help=t("arg_root"))
    p.add_argument("-o", "--output", help=t("opt_output"))
    p.add_argument("-i", "--include", action="append", metavar="GLOB", help=t("opt_include"))
    p.add_argument("-x", "--exclude", action="append", metavar="GLOB", help=t("opt_exclude"))
    p.add_argument("--no-gitignore", action="store_true", help=t("opt_no_gitignore"))
    p.add_argument("--no-tree", action="store_true", help=t("opt_no_tree"))
    p.add_argument("--no-content", action="store_true", help=t("opt_no_content"))
    p.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS, help=t("opt_max_tokens"))
    p.add_argument(
        "--max-file-chars", type=int, default=200_000, help="Skip files larger than this many chars"
    )
    p.add_argument("--model", default="gpt-4o", help=t("opt_model"))
    p.add_argument("--copy", action="store_true", help=t("opt_copy"))
    p.add_argument("--json", action="store_true", help=t("opt_json"))
    p.add_argument("--list", action="store_true", help=t("opt_list"))
    p.add_argument("-v", "--version", action="version", version=f"repo2prompt {__version__}")
    p.add_argument("--lang", help=t("opt_lang_choices") + " (env: R2P_LANG)")
    return p


def _write_stdout(text):
    with contextlib.suppress(Exception):  # nosec B110
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")
    except UnicodeEncodeError:
        sys.stdout.buffer.write(text.encode("utf-8", "replace"))
        if not text.endswith("\n"):
            sys.stdout.buffer.write(b"\n")


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    with contextlib.suppress(Exception):  # nosec B110
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    if args.lang:
        set_lang(args.lang)

    result = pack(
        args.path,
        include=args.include,
        exclude=args.exclude,
        max_tokens=args.max_tokens,
        no_tree=args.no_tree,
        no_content=args.no_content,
        respect_gitignore=not args.no_gitignore,
        token_model=args.model,
        max_file_chars=args.max_file_chars,
    )

    if args.list:
        for e in result.entries:
            if e.content and not e.reason:
                print(e.relpath)
        return 0

    if args.json:
        stats = {
            "root": result.root_path,
            "total_files": len(result.entries),
            "included_files": sum(1 for e in result.entries if e.content and not e.reason),
            "total_tokens": result.total_tokens,
            "included_tokens": result.included_tokens,
            "token_mode": result.token_mode,
            "truncated": result.truncated,
        }
        print(json.dumps(stats, ensure_ascii=False, indent=2))

    out = result.markdown
    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(
            f"{t('output_written')} {args.output} "
            f"({result.included_tokens:,} {t('output_tokens')}, "
            f"{len(result.entries)} {t('output_files')})",
            file=sys.stderr,
        )
    else:
        if args.copy:
            try:
                import pyperclip  # type: ignore

                pyperclip.copy(out)
                print(t("output_copied"), file=sys.stderr)
            except Exception as ex:  # pragma: no cover
                print(f"Clipboard unavailable ({ex}).", file=sys.stderr)
        _write_stdout(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
