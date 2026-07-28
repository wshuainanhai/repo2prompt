from pathlib import Path

from repo2prompt.packer import pack


def _make_repo(tmp_path: Path) -> Path:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("def main():\n    pass\n")
    (tmp_path / "README.md").write_text("# Hi\n")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "x.js").write_text("ignored")
    (tmp_path / "logo.png").write_text("binarybytes")
    return tmp_path


def test_pack_basic(tmp_path):
    _make_repo(tmp_path)
    res = pack(tmp_path)
    md = res.markdown
    # included files are present
    assert "src/main.py" in md
    assert "README.md" in md
    # binary files are skipped (listed in the Skipped section)
    assert "binary" in md
    # real python content is embedded; gitignored dirs are pruned entirely
    assert "def main()" in md
    assert "x.js" not in md  # node_modules content must not be embedded
    assert res.included_tokens > 0
    assert res.total_files >= 2


def test_pack_include_filter(tmp_path):
    _make_repo(tmp_path)
    res = pack(tmp_path, include=["*.py"])
    assert any(e.relpath.endswith(".py") for e in res.entries if e.content)
    assert all((e.relpath.endswith(".py") or not e.content) for e in res.entries)


def test_pack_exclude_and_tree(tmp_path):
    res = pack(tmp_path, exclude=["README.md"], no_tree=False)
    assert "README.md" not in res.markdown or "Skipped" in res.markdown
    assert "Directory Structure" in res.markdown


def test_pack_max_tokens(tmp_path):
    big = "x = 1\n" * 5000
    (tmp_path / "big.py").write_text(big)
    res = pack(tmp_path, max_tokens=10)
    assert res.truncated is True
    assert "Skipped Files" in res.markdown
