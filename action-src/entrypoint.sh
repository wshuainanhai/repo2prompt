#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# repo2prompt GitHub Action — entrypoint
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

# Inputs (provided by GitHub Action runner)
INPUT_ROOT="${INPUT_ROOT:-.}"
INPUT_OUTPUT="${INPUT_OUTPUT:-repo-context.md}"
INPUT_INCLUDE="${INPUT_INCLUDE:-}"
INPUT_EXCLUDE="${INPUT_EXCLUDE:-}"
INPUT_MAX_TOKENS="${INPUT_MAX_TOKENS:-10000}"
INPUT_LANG="${INPUT_LANG:-en}"
INPUT_NO_TREE="${INPUT_NO_TREE:-false}"
INPUT_NO_CONTENT="${INPUT_NO_CONTENT:-false}"
INPUT_NO_GITIGNORE="${INPUT_NO_GITIGNORE:-false}"
INPUT_JSON="${INPUT_JSON:-false}"

echo "::group::📦 repo2prompt"
echo "  Root:       $INPUT_ROOT"
echo "  Output:     $INPUT_OUTPUT"
echo "  Include:    ${INPUT_INCLUDE:-<all>}"
echo "  Exclude:    ${INPUT_EXCLUDE:-<none>}"
echo "  Max tokens: $INPUT_MAX_TOKENS"
echo "  Language:   $INPUT_LANG"
echo "::endgroup::"

# Build command
CMD=(python -m repo2prompt "$INPUT_ROOT" -o "$INPUT_OUTPUT")
[[ "$INPUT_NO_TREE"    == "true" ]] && CMD+=(--no-tree)
[[ "$INPUT_NO_CONTENT" == "true" ]] && CMD+=(--no-content)
[[ "$INPUT_NO_GITIGNORE" == "true" ]] && CMD+=(--no-gitignore)
[[ "$INPUT_JSON"       == "true" ]] && CMD+=(--json)

[[ -n "$INPUT_INCLUDE" ]] && IFS=',' read -ra GLOBS <<< "$INPUT_INCLUDE" && \
  for g in "${GLOBS[@]}"; do CMD+=(--include "$(echo $g | xargs)"); done

[[ -n "$INPUT_EXCLUDE" ]] && IFS=',' read -ra GLOBS <<< "$INPUT_EXCLUDE" && \
  for g in "${GLOBS[@]}"; do CMD+=(--exclude "$(echo $g | xargs)"); done

CMD+=(--max-tokens "$INPUT_MAX_TOKENS")
CMD+=(--lang "$INPUT_LANG")

echo "Running: ${CMD[*]}"
"${CMD[@]}"

if [[ -s "$INPUT_OUTPUT" ]]; then
  SIZE=$(wc -c < "$INPUT_OUTPUT")
  echo "✅ repo2prompt complete — wrote $SIZE bytes → $INPUT_OUTPUT"
  echo "output-path=$INPUT_OUTPUT" >> "$GITHUB_OUTPUT"
  echo "output-size=$SIZE" >> "$GITHUB_OUTPUT"
else
  echo "::error::repo2prompt produced an empty output"
  exit 1
fi
