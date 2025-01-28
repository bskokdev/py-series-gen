import pytest
from publishers.targets import FileTarget, FileType


def test_invalid_file_path():
    with pytest.raises(ValueError) as exc_info:
        FileTarget(file_path="", batch_size=120, is_stream=False)

    assert "Valid file path has to be specified (--path FILE_PATH)" in str(
        exc_info.value
    )


def test_determine_file_type():
    csv_file_target = FileTarget(
        file_path="/directory/file.csv", batch_size=120, is_stream=False
    )

    assert csv_file_target.file_type == FileType.CSV

    with pytest.raises(ValueError) as exc_info:
        FileTarget(file_path="/directory/file.random", batch_size=120, is_stream=False)

    assert "Not supported extension, or invalid file path was provided" in str(
        exc_info.value
    )
