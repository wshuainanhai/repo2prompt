"""Token estimation for repo2prompt.

Uses tiktoken when available (accurate), otherwise falls back to a
characters/4 heuristic (approximate, good enough for budgeting).
"""
from __future__ import annotations


class TokenCounter:
    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self._enc = None
        self._mode = "chars"
        try:
            import tiktoken  # type: ignore

            try:
                self._enc = tiktoken.encoding_for_model(model)
            except Exception:
                self._enc = tiktoken.get_encoding("cl100k_base")
            self._mode = "tiktoken"
        except Exception:
            self._mode = "chars"

    def count(self, text: str) -> int:
        if self._mode == "tiktoken" and self._enc is not None:
            return len(self._enc.encode(text))
        if not text:
            return 0
        return max(1, int(len(text) / 4))

    def mode(self) -> str:
        return self._mode
