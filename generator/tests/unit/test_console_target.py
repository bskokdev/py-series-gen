import pytest
from publishers.targets import ConsoleTarget


# NOTE: this test can be generalized to all target implementations
# as the batch_size validation is part of the abstract Target class
def test_invalid_batch_size():
    with pytest.raises(ValueError) as exc_info:
        ConsoleTarget(batch_size=-1, is_stream=False)
    assert "Batch size must be specified (--batch-size SIZE | SIZE > 0)" in str(
        exc_info.value
    )
