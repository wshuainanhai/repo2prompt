from repo2prompt.tree import build_tree


def test_build_tree_nested():
    paths = ["src/main.py", "src/util/helper.py", "README.md"]
    tree = build_tree(paths)
    assert "├── README.md" in tree
    assert "src" in tree
    assert "main.py" in tree
    assert "helper.py" in tree


def test_build_tree_empty():
    assert build_tree([]) == ""
