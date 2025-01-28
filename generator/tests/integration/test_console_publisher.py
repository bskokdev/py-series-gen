import pytest

from .integration import run_integration


@pytest.mark.integration_test
def test_console_publisher(capsys, monkeypatch):
    batch_size = 2048
    args = ["test.py", "--target", "console", "--batch-size", str(batch_size)]

    # this modifies the runtime arguments programatically
    monkeypatch.setattr("sys.argv", args)
    run_integration()

    # capsys spies on the std, and reads the output (.out)
    output = capsys.readouterr().out

    assert output

    lines = output.splitlines()
    assert len(lines) == batch_size
    for i, row in enumerate(lines):
        assert row == f"[{i}, {i+1}, {i+2}]"
