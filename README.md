# PySeriesGen - Python Data Generator
A flexible Python-based data generation tool that creates and publishes data streams using Python generators. This tool is designed to be extensible and configurable through command-line arguments, and custom generator functions.

## Features
- 🔄 Streaming data generation using Python generator functions (only time series generator available for now)
- 🎯 Multiple publish targets support (currently Console, and Kafka)
- ⚡ Efficient batch processing
- 🛠️ Configurable through CLI arguments
- 🔌 Extensible architecture for adding new publish targets

## Installation
```bash
# Clone the repository
git clone https://github.com/bskokdev/py-series-gen.git

# Navigate to the generator directory
cd py-series-gen/generator

# Install dependencies
# Consider creating a virtual environment before running this step
pip install -r requirements.txt
```

## Usage

#### Default Arguments
`--target <TARGET_TYPE>` - Specifies the publish target (e.g., console, kafka)
`--batch-size <DATA_SIZE>` - Sets the size of data batches to generate
`--stream` - Enables streaming mode. For now this means, the batches are sent repeatedly to the target.

#### Kafka Arguments
`--bootstrap-server <SERVER_ADDRESS>` - Tells the program where is the Kafka bootstrap-server running
`--port <PORT>` - On which port the bootstrap-server runs
`--topic <KAFKA TOPIC>` - Specifies the topic the data should be generated to

If you more need help, you can use `--help` argument to view all supported arguments, and usages.

## Scripts for you to use
I have included some helpful scripts directly in the repository which you can run (check out `generator/scripts` directory).

- `generate.sh` - Generates data with `batch_size=2048` to the `console` target
- `typecheck.sh` - Uses MyPy to statically check types in the entire repository 
- `unit-tests.sh` - Runs unit tests (marked with `@pytest.mark.unit_test` decorator)
- `integration-tests.sh` - Runs integration tests (marked with `@pytest.mark.integration_test` decorator)


### Examples
```bash
# Stream batches of data to the console, each batch contains 2048 values
python3 py_series_gen.py --target console --batch-size 2048 --stream

# Generate a single batch of 1000 values to the console
python3 py_series_gen.py --target console --batch-size 1000

# Stream batches of size 32 to the `py-topic` Kafka topic which is present at localhost:9092
python3 py_series_gen.py --target kafka --batch-size 32 --bootstrap-server localhost --port 9092 --topic py-topic --stream
```

### Architecture
The generator is built with a modular architecture (see docs for more). The 3 main concepts are Publishers, Targets, and generator functions. Both Publishers, and Targers are generated dynamically from the CLI arguments by their respective factories. The generator functions are implemented for each supported publish target.

- Publish Targets: Handle the state for different destinations
- PublisherFactory: Creates appropriate publisher instances based on target
- Generator Functions: Produce the actual data (e.g., time_series_generator)

### Extending
For adding new targets:
1. Create a new target class implementing the target interface
2. Register the new target in the factory
3. Add CLI support for the new target

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.