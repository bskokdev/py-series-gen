import pytest
from publishers.targets import KafkaTarget


@pytest.mark.unit_test
def test_missing_bootstrap_server():
    with pytest.raises(ValueError) as exc_info:
        KafkaTarget(
            kafka_topic="test-topic",
            bootstrap_server=None,
            server_port=9092,
            batch_size=32,
            is_stream=False,
        )
    assert "Bootstrap server has to be specified" in str(exc_info.value)


@pytest.mark.unit_test
def test_empty_bootstrap_server():
    with pytest.raises(ValueError) as exc_info:
        KafkaTarget(
            kafka_topic="test-topic",
            bootstrap_server="",
            server_port=9092,
            batch_size=32,
            is_stream=False,
        )
    assert "Bootstrap server has to be specified" in str(exc_info.value)


@pytest.mark.unit_test
def test_missing_kafka_topic():
    with pytest.raises(ValueError) as exc_info:
        KafkaTarget(
            kafka_topic=None,
            bootstrap_server="localtest",
            server_port=9092,
            batch_size=32,
            is_stream=False,
        )
    assert "Kafka topic has to be specified" in str(exc_info.value)


@pytest.mark.unit_test
def test_empty_kafka_topic():
    with pytest.raises(ValueError) as exc_info:
        KafkaTarget(
            kafka_topic="",
            bootstrap_server="localtest",
            server_port=9092,
            batch_size=32,
            is_stream=False,
        )
    assert "Kafka topic has to be specified" in str(exc_info.value)


@pytest.mark.unit_test
def test_missing_server_port():
    with pytest.raises(ValueError) as exc_info:
        KafkaTarget(
            kafka_topic="test-topic",
            bootstrap_server="localtest",
            server_port=None,
            batch_size=32,
            is_stream=False,
        )
    assert "Bootstrap server's port has to be specified" in str(exc_info.value)


@pytest.mark.unit_test
def test_valid_kafka_args():
    try:
        KafkaTarget(
            kafka_topic="valid-topic",
            bootstrap_server="localtest",
            server_port=9092,
            batch_size=32,
            is_stream=False,
        )
    except:
        pytest.fail("Valid kafka arguments shouldn't raise ValueError")
