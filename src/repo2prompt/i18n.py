"""Internationalization for CLI help strings.

Detects language from the environment variable R2P_LANG (en/zh/ja/ko/fr/de/es).
Falls back to LC_MESSAGES/LANG/LANGUAGE/LC_ALL, then defaults to English.
"""

import os

DEFAULT_LANG = "en"

LANG_ENV_VARS = ["R2P_LANG", "LC_MESSAGES", "LANG", "LANGUAGE", "LC_ALL"]

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "cli_description": "Pack a repository into clean, AI-friendly context",
        "arg_root": "Root directory to scan (default: current directory)",
        "opt_output": "Write output to FILE instead of stdout",
        "opt_include": "Include only files matching GLOB (can be repeated)",
        "opt_exclude": "Exclude files matching GLOB (can be repeated)",
        "opt_no_gitignore": "Do not respect .gitignore files",
        "opt_no_tree": "Skip the directory tree section",
        "opt_no_content": "Skip file contents (tree only)",
        "opt_max_tokens": "Maximum tokens to include (soft cap)",
        "opt_model": "Model for token counting (cl100k_base/gpt-4/o200k_base)",
        "opt_copy": "Copy output to clipboard",
        "opt_json": "Output machine-readable JSON summary",
        "opt_lang_choices": "CLI language (en/zh/ja/ko/fr/de)",
        "opt_list": "List files without content",
        "opt_version": "Show version and exit",
        "help_version": "show version",
        "help_help": "show this help message",
        "output_copied": "Output copied to clipboard",
        "output_written": "Wrote context to",
        "output_files": "files",
        "output_tokens": "tokens",
        "skipped": "Skipped",
        "truncated": "Truncated — some files exceeded max-tokens budget",
        "reason_gitignored": "gitignored",
        "reason_binary": "binary",
        "reason_too_large": "too large",
    },
    "zh": {
        "cli_description": "将任意仓库一键打包成 AI 友好的上下文",
        "arg_root": "要扫描的根目录（默认当前目录）",
        "opt_output": "输出到文件而非 stdout",
        "opt_include": "仅包含匹配 GLOB 的文件（可重复）",
        "opt_exclude": "排除匹配 GLOB 的文件（可重复）",
        "opt_no_gitignore": "不遵守 .gitignore",
        "opt_no_tree": "跳过目录树部分",
        "opt_no_content": "跳过文件内容（仅目录树）",
        "opt_max_tokens": "最大 token 数量（软上限）",
        "opt_model": "用于 token 计数的模型（cl100k_base/gpt-4/o200k_base）",
        "opt_copy": "复制输出到剪贴板",
        "opt_json": "输出机器可读的 JSON 摘要",
        "opt_list": "仅列出文件（不含内容）",
        "opt_version": "显示版本并退出",
        "help_version": "显示版本",
        "help_help": "显示帮助",
        "output_copied": "已复制到剪贴板",
        "output_written": "上下文已写入",
        "output_files": "个文件",
        "output_tokens": "tokens",
        "skipped": "已跳过",
        "truncated": "已截断 — 部分文件超出最大 token 预算",
        "reason_gitignored": "被 gitignore 忽略",
        "reason_binary": "二进制文件",
        "reason_too_large": "文件过大",
    },
    "ja": {
        "cli_description": "リポジトリをAIに優しいコンテキストにパック",
        "arg_root": "スキャンするルートディレクトリ（デフォルト: 現在地）",
        "opt_output": "出力をstdoutではなくFILEに書き込む",
        "opt_include": "GLOBに一致するファイルのみを含める（繰り返し可）",
        "opt_exclude": "GLOBに一致するファイルを除外（繰り返し可）",
        "opt_no_gitignore": ".gitignoreを無視する",
        "opt_no_tree": "ディレクトリツリーセクションをスキップ",
        "opt_no_content": "ファイル内容をスキップ（ツリーのみ）",
        "opt_max_tokens": "含む最大トークン数（ソフト上限）",
        "opt_model": "トークン計数用モデル（cl100k_base/gpt-4/o200k_base）",
        "opt_copy": "出力をクリップボードにコピー",
        "opt_json": "機械可読なJSONサマリーを出力",
        "opt_list": "内容の代わりにファイル一覧を表示",
        "opt_version": "バージョンを表示して終了",
        "help_version": "バージョンを表示",
        "help_help": "このヘルプメッセージを表示",
        "output_copied": "出力をクリップボードにコピーしました",
        "output_written": "コンテキストを書き込みました",
        "output_files": "ファイル",
        "output_tokens": "トークン",
        "skipped": "スキップ",
        "truncated": "トランケート — 一部のファイルがトークン上限を超えました",
        "reason_gitignored": "gitignore対象",
        "reason_binary": "バイナリ",
        "reason_too_large": "サイズ超過",
    },
    "ko": {
        "cli_description": "AI 친화적 컨텍스트로 저장소를 패킹",
        "arg_root": "스캔할 루트 디렉토리 (기본값: 현재 디렉토리)",
        "opt_output": "출력을 stdout 대신 FILE에 쓰기",
        "opt_include": "GLOB과 일치하는 파일만 포함 (반복 가능)",
        "opt_exclude": "GLOB과 일치하는 파일 제외 (반복 가능)",
        "opt_no_gitignore": ".gitignore를 무시",
        "opt_no_tree": "디렉토리 트리 섹션 건너뛰기",
        "opt_no_content": "파일 내용 건너뛰기 (트리만)",
        "opt_max_tokens": "포함할 최대 토큰 수 (소프트 상한)",
        "opt_model": "토큰 계산용 모델 (cl100k_base/gpt-4/o200k_base)",
        "opt_copy": "출력을 클립보드에 복사",
        "opt_json": "머신 읽기 가능한 JSON 요약 출력",
        "opt_list": "내용 대신 파일 목록만 표시",
        "opt_version": "버전을 표시하고 종료",
        "help_version": "버전 표시",
        "help_help": "이 도움말 메시지 표시",
        "output_copied": "출력이 클립보드에 복사됨",
        "output_written": "컨텍스트를 작성했습니다",
        "output_files": "파일",
        "output_tokens": "토큰",
        "skipped": "건너뜀",
        "truncated": "트렁케이트됨 — 일부 파일이 최대 토큰 예산 초과",
        "reason_gitignored": "gitignore 대상",
        "reason_binary": "바이너리",
        "reason_too_large": "크기 초과",
    },
    "fr": {
        "cli_description": "Emballez un dépôt en un contexte propre et adapté à l'IA",
        "arg_root": "Répertoire racine à analyser (défaut : répertoire courant)",
        "opt_output": "Écrire la sortie dans FILE au lieu de stdout",
        "opt_include": "Inclure uniquement les fichiers correspondant à GLOB",
        "opt_exclude": "Exclure les fichiers correspondant à GLOB",
        "opt_no_gitignore": "Ne pas respecter les fichiers .gitignore",
        "opt_no_tree": "Omettre la section arborescence",
        "opt_no_content": "Omettre le contenu des fichiers (arbre seul)",
        "opt_max_tokens": "Nombre maximum de tokens (plafond souple)",
        "opt_model": "Modèle pour le comptage de tokens",
        "opt_copy": "Copier la sortie dans le presse-papiers",
        "opt_json": "Sortir un résumé JSON lisible par machine",
        "opt_list": "Lister les fichiers sans leur contenu",
        "opt_version": "Afficher la version et quitter",
        "help_version": "afficher la version",
        "help_help": "afficher ce message d'aide",
        "output_copied": "Sortie copiée dans le presse-papiers",
        "output_written": "Contexte écrit dans",
        "output_files": "fichiers",
        "output_tokens": "tokens",
        "skipped": "Ignoré(s)",
        "truncated": "Tronqué — certains fichiers dépassent le budget token",
        "reason_gitignored": "ignoré par gitignore",
        "reason_binary": "binaire",
        "reason_too_large": "trop volumineux",
    },
    "de": {
        "cli_description": "Ein Repository in einen sauberen, KI-freundlichen Kontext packen",
        "arg_root": "Wurzelverzeichnis zum Scannen (Standard: aktuelles Verzeichnis)",
        "opt_output": "Ausgabe in FILE statt stdout schreiben",
        "opt_include": "Nur Dateien einschließen, die GLOB entsprechen",
        "opt_exclude": "Dateien ausschließen, die GLOB entsprechen",
        "opt_no_gitignore": ".gitignore-Dateien nicht berücksichtigen",
        "opt_no_tree": "Verzeichnisbaum-Abschnitt überspringen",
        "opt_no_content": "Dateiinhalte überspringen (nur Baum)",
        "opt_max_tokens": "Maximale Anzahl an Tokens (weiche Obergrenze)",
        "opt_model": "Modell für Token-Zählung",
        "opt_copy": "Ausgabe in Zwischenablage kopieren",
        "opt_json": "Maschinenlesbares JSON-Zusammenfassung ausgeben",
        "opt_list": "Dateien ohne Inhalt auflisten",
        "opt_version": "Version anzeigen und beenden",
        "help_version": "Version anzeigen",
        "help_help": "Diese Hilfemeldung anzeigen",
        "output_copied": "Ausgabe in Zwischenablage kopiert",
        "output_written": "Kontext geschrieben nach",
        "output_files": "Dateien",
        "output_tokens": "Tokens",
        "skipped": "Übersprungen",
        "truncated": "Gekürzt — einige Dateien überschreiten das Token-Budget",
        "reason_gitignored": "gitignored",
        "reason_binary": "Binärdatei",
        "reason_too_large": "zu groß",
    },
}

# ── helpers ──────────────────────────────────────────────────────────────────


def _detect_lang() -> str:
    """Detect language from environment, returning a supported lang or 'en'."""
    for var in LANG_ENV_VARS:
        val = os.environ.get(var, "")
        if not val:
            continue
        # e.g. "en_US.UTF-8" → "en"; "zh_CN" → "zh"
        lang = val.split("_")[0].split(".")[0].lower()
        if lang in TRANSLATIONS:
            return lang
        # also accept full locale prefix if TRANSLATIONS has it
        if val in TRANSLATIONS:
            return val
    return DEFAULT_LANG


# Module-level singleton
_current_lang: str | None = None


def t(key: str) -> str:
    """Translate key into current language, falling back to English."""
    global _current_lang
    if _current_lang is None:
        _current_lang = _detect_lang()
    return TRANSLATIONS.get(_current_lang, TRANSLATIONS[DEFAULT_LANG]).get(
        key, TRANSLATIONS[DEFAULT_LANG].get(key, key)
    )


def set_lang(lang: str) -> None:
    """Force the current language (e.g. from CLI --lang flag)."""
    global _current_lang
    _current_lang = lang if lang in TRANSLATIONS else DEFAULT_LANG
