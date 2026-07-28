"""Gitignore-aware path filtering for repo2prompt.

Uses `pathspec` when available (full gitwildmatch fidelity) and falls back to a
small built-in matcher so the tool still works with zero dependencies.
"""

from __future__ import annotations

import re
from pathlib import Path

# Common junk that should be skipped even without a .gitignore present.
DEFAULT_IGNORE: list[str] = [
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "env",
    ".env",
    "dist",
    "build",
    ".idea",
    ".vscode",
    "*.egg-info",
    ".mypy_cache",
    ".pytest_cache",
    ".tox",
    "site-packages",
    "target",
]

# Extensions we never read (treated as binary).
BINARY_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".ico",
    ".webp",
    ".avif",
    ".pdf",
    ".zip",
    ".gz",
    ".tar",
    ".tgz",
    ".rar",
    ".7z",
    ".bz2",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".bin",
    ".o",
    ".obj",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
    ".otf",
    ".mp4",
    ".mp3",
    ".wav",
    ".mov",
    ".avi",
    ".mkv",
    ".flac",
    ".m4a",
    ".pyc",
    ".pyo",
    ".class",
    ".db",
    ".sqlite",
    ".sqlite3",
    ".wasm",
    ".rlib",
    ".a",
}


def _glob_to_regex(pat: str) -> str:
    out: list[str] = []
    i = 0
    while i < len(pat):
        c = pat[i]
        if c == "*":
            if pat[i : i + 2] == "**":
                out.append(".*")
                i += 2
                continue
            out.append("[^/]*")
            i += 1
            continue
        if c == "?":
            out.append("[^/]")
            i += 1
            continue
        out.append(re.escape(c))
        i += 1
    return "".join(out)


class PathSpecMatcher:
    """Matcher backed by pathspec (preferred)."""

    def __init__(self, patterns: list[str]):
        import pathspec  # imported lazily; only when available

        self.spec = pathspec.PathSpec.from_lines("gitignore", patterns)

    def is_ignored(self, relpath: str, is_dir: bool = False) -> bool:
        p = relpath
        if is_dir and not p.endswith("/"):
            p += "/"
        return self.spec.match_file(p)


class FallbackMatcher:
    """Minimal gitwildmatch matcher used when pathspec is unavailable."""

    def __init__(self, patterns: list[str]):
        self.rules: list[tuple] = []
        for raw in patterns:
            raw = raw.strip()
            if not raw or raw.startswith("#"):
                continue
            negated = raw.startswith("!")
            if negated:
                raw = raw[1:]
            dir_only = raw.endswith("/")
            raw2 = raw.rstrip("/")
            anchored = raw2.startswith("/")
            raw2 = raw2.lstrip("/")
            no_slash = "/" not in raw2
            rx = _glob_to_regex(raw2)
            if anchored:
                full = re.compile("^" + rx + "(?:/.*)?$")
            else:
                full = re.compile("^(?:.*/)?" + rx + "(?:/.*)?$")
            self.rules.append((full, negated, dir_only, no_slash, rx))

    def is_ignored(self, relpath: str, is_dir: bool = False) -> bool:
        ignored = False
        for full, negated, dir_only, no_slash, rx in self.rules:
            if dir_only and not is_dir:
                continue
            matched = full.match(relpath) is not None
            if not matched and no_slash:
                base = relpath.rsplit("/", 1)[-1]
                if re.match("^" + rx + "$", base):
                    matched = True
                else:
                    for comp in relpath.split("/"):
                        if re.match("^" + rx + "$", comp):
                            matched = True
                            break
            if matched:
                ignored = not negated
        return ignored


def load_matcher(root, use_gitignore: bool = True):
    """Build a matcher from DEFAULT_IGNORE plus the repo's .gitignore."""
    patterns: list[str] = list(DEFAULT_IGNORE)
    if use_gitignore:
        gi = Path(root) / ".gitignore"
        if gi.is_file():
            patterns.extend(
                line.strip()
                for line in gi.read_text(encoding="utf-8", errors="ignore").splitlines()
            )
    try:
        return PathSpecMatcher(patterns)
    except Exception:
        return FallbackMatcher(patterns)
