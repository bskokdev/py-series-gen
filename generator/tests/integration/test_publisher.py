import pytest

from cli.arguments import build_target_from_args
from publishers.publisher_factory import PublisherFactory
from values import Value


@pytest.mark.parametrize(
    "publisher_config",
    [
        {
            "name": "console",
            "args": ["test.py", "--target", "console", "--batch-size", "2048"],
            "batch_size": 2048,
            # this lamba function verifies the correct output, based on the passed parameters (output, batch_size)
            # if all are true, it evaluates to true, so the assertion passes in the test
            "verify_output": lambda output, batch_size: (
                "0" in output
                and str(batch_size - 1) in output
                and len(output.splitlines()) == batch_size
            ),
        },
        # Add other test cases below for different publish targets (file, kafka, etc.)
        # Example for a file publisher
        # {
        #     "name": "file",
        #     "args": ["main.py", "--target", "file", "--batch-size", "1024", "--output-path", "test.txt"],
        #     "batch_size": 1024,
        #     "verify_output": lambda output, batch_size: (
        #         os.path.exists("test.txt")
        #         and len(open("test.txt").readlines()) == batch_size
        #     ),
        # },
        # Example for a kafka publisher
        # {
        #     "name": "kafka",
        #     "args": ["main.py", "--target", "kafka", "--batch-size", "512", "--topic", "test"],
        #     "batch_size": 512,
        #     "verify_output": lambda output, batch_size: verify_kafka_messages(batch_size),
        # },
    ],
)
@pytest.mark.integration_test
def test_publisher_integration(publisher_config, capsys, monkeypatch):
    # this modifies the runtime arguments to the ones set in the publisher_config
    monkeypatch.setattr("sys.argv", publisher_config["args"])

    target = build_target_from_args()
    publisher = PublisherFactory().create_publisher(
        generator_func=lambda batch_s: [Value(data=i) for i in range(batch_s)],
        target=target,
    )
    publisher.publish_to_target()

    # capsys spies on the std, and reads the output (.out)
    output = capsys.readouterr().out

    assert output is not None

    # this calls a verification function defined by the "verify_output" key in the parameters,
    # and apsses the spied output, and batch_size from the config as parameters
    assert publisher_config["verify_output"](output, publisher_config["batch_size"])
