# Task Summary: repo2prompt i18n + Languages

## Completed

### Task A — `src/repo2prompt/i18n.py`
- Created internationalization module with 6 supported languages: en, zh, ja, ko, fr, de
- Language detection order: `R2P_LANG` env var → `LC_MESSAGES` → `LANG` → `LANGUAGE` → `LC_ALL` → default English
- Exports: `t(key)` — translate key to current language; `set_lang(lang)` — force a language; `TRANSLATIONS`, `LANG_ENV_VARS`, `DEFAULT_LANG`
- 25 translation keys covering CLI descriptions, arguments, options, output messages, and skip reasons
- Verified: compiles + imports cleanly; `t()` returns correct strings for zh/ja/en

### Task B — `src/repo2prompt/languages.py`
- Created extended language detection with 49 languages registered in `LANGUAGES`
- `Language` dataclass: name, extensions, patterns, single/multi comment markers, mime_prefix, `match(path)` method
- Languages covered: Python, JS/TS/JSX/TSX, Vue, Svelte, HTML, CSS/SCSS/Less, JSON/YAML/TOML/INI, Markdown/reStructuredText/AsciiDoc, Java/Kotlin/Scala/Groovy, C/C++/C#, Go, Rust, Swift, Objective-C, Ruby, PHP, Shell/PowerShell/Batch, SQL, R, Julia, Lua, Dart, Zig, Nim, Crystal, Terraform/HCL, Dockerfile, GraphQL, XML/Protobuf, Plain Text, and more
- `detect_language(path)` — returns best-matching `Language` or None; prefers extension-based matches over pattern-only
- `fenced(lang, path_str)` — returns common code-fence label (e.g. "bash" for Shell, "hcl" for Terraform/HCL)
- Verified: compiles + imports; `detect_language` correctly identifies `.py`, `package.json`, `Makefile`; `fenced()` returns correct aliases

### Files written
| File | Size |
|------|------|
| `src/repo2prompt/i18n.py` | ~9 KB |
| `src/repo2prompt/languages.py` | ~13 KB + `# Total languages: 49` |

Both pass `python3 -m py_compile` with no errors.
