import json

from stock.cli import main


def test_add_then_file(tmp_path):
    f = tmp_path / "s.json"
    f.write_text("{}")
    assert main(["--file", str(f), "add", "bolt", "3"]) == 0
    assert json.loads(f.read_text()) == {"bolt": 3}
