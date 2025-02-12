import pytest
from publishers.targets import FileTarget, FileType


@pytest.mark.unit_test
def test_empty_file_path():
    with pytest.raises(ValueError) as exc_info:
        FileTarget(file_path="", batch_size=120, is_stream=False)

    assert "Valid file path has to be specified (--path FILE_PATH)" in str(
        exc_info.value
    )


@pytest.mark.unit_test
def test_directory_file_path(tmpdir):
    with pytest.raises(ValueError) as exc_info:
        FileTarget(file_path=tmpdir, batch_size=420, is_stream=False)

    assert (
        "Directory path is not supported, provide path to a file (~/dir/file.csv)"
        in str(exc_info)
    )


@pytest.mark.unit_test
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


@pytest.mark.unit_test
def test_valid_file_path(tmp_path):
    try:
        file_path = tmp_path.absolute().as_posix() + "test_data.csv"
        FileTarget(file_path=file_path, batch_size=10, is_stream=False)
    except ValueError:
        pytest.fail("Valid batch size should not raise a ValueError")
