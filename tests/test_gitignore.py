from pathlib import Path

from repo2prompt.gitignore import load_matcher


def test_default_ignores(tmp_path):
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "x.js").write_text("x")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("print(1)")
    m = load_matcher(tmp_path, use_gitignore=False)
    assert m.is_ignored("node_modules", is_dir=True)
    assert m.is_ignored("node_modules/x.js", is_dir=False)
    assert not m.is_ignored("src/main.py", is_dir=False)


def test_gitignore_file(tmp_path):
    (tmp_path / ".gitignore").write_text("secret.txt\nbuild/\n")
    (tmp_path / "secret.txt").write_text("x")
    (tmp_path / "build").mkdir()
    (tmp_path / "build" / "out.js").write_text("x")
    (tmp_path / "keep.py").write_text("x")
    m = load_matcher(tmp_path, use_gitignore=True)
    assert m.is_ignored("secret.txt", is_dir=False)
    assert m.is_ignored("build", is_dir=True)
    assert m.is_ignored("build/out.js", is_dir=False)
    assert not m.is_ignored("keep.py", is_dir=False)


def test_negation(tmp_path):
    (tmp_path / ".gitignore").write_text("*.log\n!important.log\n")
    (tmp_path / "a.log").write_text("x")
    (tmp_path / "important.log").write_text("x")
    m = load_matcher(tmp_path, use_gitignore=True)
    assert m.is_ignored("a.log", is_dir=False)
    assert not m.is_ignored("important.log", is_dir=False)
