import pytest

from .integration import run_integration


@pytest.mark.integration_test
def test_file_publisher(tmp_path, monkeypatch):
    batch_size = 512
    file_path = tmp_path.absolute().as_posix() + "test_data.csv"
    args = [
        "test.py",
        "--target",
        "file",
        "--path",
        file_path,
        "--batch-size",
        str(batch_size),
    ]
    monkeypatch.setattr("sys.argv", args)
    run_integration()

    assert file_path
    with open(file_path, "r") as file:
        line_cnt = 0
        for i, row in enumerate(file):
            line_cnt += 1
            assert row == f"{i};{i+1};{i+2}\n"

        assert line_cnt == batch_size
