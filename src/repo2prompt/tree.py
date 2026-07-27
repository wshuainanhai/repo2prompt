"""Directory-tree rendering for repo2prompt."""
from __future__ import annotations


def build_tree(paths):
    """Render a list of relative posix paths into an ASCII tree."""
    root: dict = {}
    for p in paths:
        node = root
        for part in p.split("/"):
            if part == "":
                continue
            node = node.setdefault(part, {})

    lines: list = []

    def render(node, prefix=""):
        entries = sorted(node.keys())
        for i, name in enumerate(entries):
            last = i == len(entries) - 1
            connector = "└── " if last else "├── "
            lines.append(prefix + connector + name)
            child_prefix = prefix + ("    " if last else "│   ")
            render(node[name], child_prefix)

    render(root)
    return "\n".join(lines)
