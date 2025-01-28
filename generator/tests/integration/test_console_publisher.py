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

    assert output is not None

    assert "0" in output
    assert str(batch_size - 1) in output
    assert len(output.splitlines()) == batch_size
