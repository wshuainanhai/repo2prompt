"""Extended programming language detection from file paths.

Covers: standard, framework-specific, config, markup, data, infrastructure,
and niche languages that are common in real-world repos but missed by naive
extensions-based detection.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import PurePath

# ── types ─────────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Language:
    name: str  # display name
    extensions: tuple[str, ...]  # e.g. (".py",)
    patterns: tuple[str, ...]  # regex patterns for filename matching
    single_comment: str = "#"
    multi_comment_start: str = '"""'
    multi_comment_end: str = '"""'
    mime_prefix: str = "text/x-"

    def match(self, path: PurePath) -> bool:
        name = path.name.lower()
        return any(name.endswith(ext) for ext in self.extensions) or any(
            re.match(pat, name) for pat in self.patterns
        )


# ── language registry ──────────────────────────────────────────────────────────

LANGUAGES: list[Language] = [
    Language(
        name="Python",
        extensions=(".py", ".pyi"),
        patterns=(),
        single_comment="#",
        multi_comment_start='"""',
        multi_comment_end='"""',
    ),
    Language(
        name="JavaScript",
        extensions=(".js", ".mjs", ".cjs"),
        patterns=("^package\\.json$",),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="TypeScript",
        extensions=(".ts", ".mts", ".cts"),
        patterns=("^tsconfig\\.json$",),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="JSX",
        extensions=(".jsx",),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="TSX",
        extensions=(".tsx",),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="Vue",
        extensions=(".vue",),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="Svelte",
        extensions=(".svelte",),
        patterns=(),
        single_comment="//",
        multi_comment_start="<!--",
        multi_comment_end="-->",
    ),
    Language(
        name="HTML",
        extensions=(".html", ".htm"),
        patterns=(),
        single_comment="",
        multi_comment_start="<!--",
        multi_comment_end="-->",
    ),
    Language(
        name="CSS",
        extensions=(".css", ".ccss"),
        patterns=(),
        single_comment="",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="SCSS",
        extensions=(".scss", ".sass"),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="Less",
        extensions=(".less",),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="JSON",
        extensions=(".json", ".jsonc", ".jsonl"),
        patterns=(
            "^tsconfig.*\\.json$",
            "^package\\.json$",
            "^\\.eslintrc.*$",
            "^\\.prettierrc.*$",
            "^\\.stylelintrc.*$",
            "^vetur\\.db\\.json$",
            "^deno\\.json.*$",
            "^ import\\.map$",
        ),
        single_comment="",
        multi_comment_start="",
        multi_comment_end="",
        mime_prefix="application/json",
    ),
    Language(
        name="YAML",
        extensions=(".yaml", ".yml"),
        patterns=(
            "^\\.github/",
            "^docker-compose",
            "^Makefile$",
            "^\\.gitlab-ci\\.yml$",
            "^\\.circleci/",
            "^\\.pre-commit-config\\.yaml$",
        ),
        single_comment="#",
        multi_comment_start="",
        multi_comment_end="",
    ),
    Language(
        name="TOML",
        extensions=(".toml",),
        patterns=("^pyproject\\.toml$", "^Cargo\\.toml$", "^deno\\.toml$"),
        single_comment="#",
        multi_comment_start="",
        multi_comment_end="",
    ),
    Language(
        name="INI",
        extensions=(".ini", ".cfg", ".conf", ".properties"),
        patterns=(),
        single_comment=";",
        multi_comment_start="",
        multi_comment_end="",
    ),
    Language(
        name="Markdown",
        extensions=(".md", ".mdx", ".markdown"),
        patterns=(),
        single_comment="",
        multi_comment_start="",
        multi_comment_end="",
    ),
    Language(
        name="reStructuredText",
        extensions=(".rst",),
        patterns=(),
        single_comment="..",
        multi_comment_start="",
        multi_comment_end="",
    ),
    Language(
        name="AsciiDoc",
        extensions=(".adoc", ".asciidoc"),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="Java",
        extensions=(".java",),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="Kotlin",
        extensions=(".kt", ".kts"),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="Scala",
        extensions=(".scala",),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="Groovy",
        extensions=(".groovy", ".gradle"),
        patterns=("^Jenkinsfile$",),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="C",
        extensions=(".c", ".h"),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="C++",
        extensions=(".cpp", ".cc", ".cxx", ".hh", ".hpp", ".hxx"),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="C#",
        extensions=(".cs",),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="Go",
        extensions=(".go",),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="Rust",
        extensions=(".rs",),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="Swift",
        extensions=(".swift",),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="Objective-C",
        extensions=(".m", ".mm"),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="Ruby",
        extensions=(".rb",),
        patterns=("^Gemfile$", "^Rakefile$", "^Brewfile$"),
        single_comment="#",
        multi_comment_start="=begin",
        multi_comment_end="=end",
    ),
    Language(
        name="PHP",
        extensions=(".php",),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="Shell",
        extensions=(".sh", ".bash", ".zsh", ".fish", ".ksh", ".ash"),
        patterns=(
            "^Makefile$",
            "^\\.bashrc$",
            "^\\.zshrc$",
            "^\\.profile$",
            "^entrypoint\\.sh$",
            "^start\\.sh$",
            "^run\\.sh$",
        ),
        single_comment="#",
        multi_comment_start="",
        multi_comment_end="",
    ),
    Language(
        name="PowerShell",
        extensions=(".ps1", ".psm1", ".psd1", ".ps1xml"),
        patterns=(),
        single_comment="#",
        multi_comment_start="<#",
        multi_comment_end="#>",
    ),
    Language(
        name="Batch",
        extensions=(".bat", ".cmd"),
        patterns=(),
        single_comment="REM",
        multi_comment_start="",
        multi_comment_end="",
    ),
    Language(
        name="SQL",
        extensions=(".sql", ".dsql"),
        patterns=(),
        single_comment="--",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="R",
        extensions=(".r", ".R", ".Rmd"),
        patterns=(),
        single_comment="#",
        multi_comment_start="",
        multi_comment_end="",
    ),
    Language(
        name="Julia",
        extensions=(".jl",),
        patterns=(),
        single_comment="#",
        multi_comment_start='"""',
        multi_comment_end='"""',
    ),
    Language(
        name="Lua",
        extensions=(".lua",),
        patterns=(),
        single_comment="--",
        multi_comment_start="--[[",
        multi_comment_end="]]",
    ),
    Language(
        name="Dart",
        extensions=(".dart",),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="Zig",
        extensions=(".zig",),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="Nim",
        extensions=(".nim", ".nims"),
        patterns=(),
        single_comment="#",
        multi_comment_start="##",
        multi_comment_end="##",
    ),
    Language(
        name="Crystal",
        extensions=(".cr",),
        patterns=(),
        single_comment="#",
        multi_comment_start="=begin",
        multi_comment_end="=end",
    ),
    Language(
        name="Terraform",
        extensions=(".tf", ".tfvars"),
        patterns=(),
        single_comment="#",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="HCL",
        extensions=(".hcl", ".tf.json"),
        patterns=("^Pipfile$",),
        single_comment="#",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="Dockerfile",
        extensions=(),
        patterns=("^Dockerfile$", "^\\.dockerignore$", "^docker-compose.*\\.ya?ml$"),
        single_comment="#",
        multi_comment_start="",
        multi_comment_end="",
    ),
    Language(
        name="GraphQL",
        extensions=(".graphql", ".gql"),
        patterns=(),
        single_comment="#",
        multi_comment_start='"""',
        multi_comment_end='"""',
    ),
    Language(
        name="XML",
        extensions=(".xml", ".xsl", ".xslt", ".svg", ".xaml"),
        patterns=(),
        single_comment="",
        multi_comment_start="<!--",
        multi_comment_end="-->",
    ),
    Language(
        name="Protobuf",
        extensions=(".proto",),
        patterns=(),
        single_comment="//",
        multi_comment_start="/*",
        multi_comment_end="*/",
    ),
    Language(
        name="Plain Text",
        extensions=(".txt",),
        patterns=(
            "^README",
            "^LICENSE",
            "^CHANGELOG",
            "^AUTHORS",
            "^NOTICE",
            "^CONTRIBUTING",
            "^SECURITY",
            "^Code\\ of\\ Conduct",
        ),
        single_comment="",
        multi_comment_start="",
        multi_comment_end="",
        mime_prefix="text/plain",
    ),
]

# ── detection API ─────────────────────────────────────────────────────────────


def detect_language(path: PurePath) -> Language | None:
    """Return the best-matching Language for a file path, or None."""
    candidates = [lang for lang in LANGUAGES if lang.match(path)]
    # Prefer languages with extensions over those with only patterns (less specific)
    by_ext = [c for c in candidates if c.extensions]
    return by_ext[0] if by_ext else (candidates[0] if candidates else None)


def fenced(lang: Language | None, path_str: str = "") -> str:
    """Return the best fence label for a language (try common aliases)."""
    if lang is None:
        return _ext_fence(path_str)
    # known aliases
    alias = {
        "Shell": "bash",
        "Markdown": "markdown",
        "reStructuredText": "rst",
        "YAML": "yaml",
        "Plain Text": "text",
        "TOML": "toml",
        "INI": "ini",
        "SCSS": "scss",
        "JSX": "jsx",
        "TSX": "tsx",
        "GraphQL": "graphql",
        "Terraform": "hcl",
        "HCL": "hcl",
        "PowerShell": "powershell",
        "Batch": "bat",
        "Protobuf": "protobuf",
        "Dockerfile": "dockerfile",
    }.get(lang.name, lang.name.lower().replace(" ", "-"))
    return alias


def _ext_fence(path_str: str) -> str:
    import os

    _, ext = os.path.splitext(path_str)
    return ext.lstrip(".") if ext else "text"


# Total languages: 49
