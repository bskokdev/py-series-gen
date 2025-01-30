# PySeriesGen - Python Data Generator
A flexible Python-based data generation tool that creates and publishes data streams using Python generators. This tool is designed to be extensible and configurable through command-line arguments, and custom generator functions.

## Features
- 🔄 Streaming data generation using Python generator functions (only time series generator available for now)
- 🎯 Multiple publish targets support (Console, Kafka, CSV, HTTP)
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

## Running via Docker

There's a Dockerfile provided in `/generator` directory which builds the py-series-gen image.

```bash
# Build the docker image

docker build -t py-series-gen .

# Run the application using docker
docker run py-series-gen --help
```

## Usage

#### Default Arguments
* `--target <(console, kafka, file, http)>` - Specifies the publish target
* `--batch-size <DATA_SIZE>` - Sets the size of data batches to generate
* `--generator` - Specifies which generator function should be used to generate the data
    * currently only `time-series` generator is supported
* `--stream` - Enables streaming mode. For now this means, the batches are sent repeatedly to the given target.

#### Kafka Arguments
* `--bootstrap-server <SERVER_ADDRESS>` - Tells the program where is the Kafka bootstrap-server running
* `--port <PORT>` - On which port the bootstrap-server runs
* `--topic <KAFKA_TOPIC>` - Specifies the topic the data should be generated to

#### HTTP Arguments
* `--endpoint <ENDPOINT_URL>` - Defines the endpoint URL where the data should be published
    * **NOTE:** This has to be a valid URL!

#### File Arguments
* `--path FILE_PATH` - Specifies to which file the progam should write the data
    **NOTES**:
    * Currently supported file extensions are: `.csv`
    * The FILE_PATH cannot point to a directory
    * If the file doesn't exist yet at the destination, the progam automatically creates it

If you more need help, you can use `--help` argument to view all supported arguments, and usages.

## Testing 

For testing I've used pytest, since it has a good support for fixtures, allows custom marks, and is generally very simple to use, and provides more features than the unittest Python module. 

Currently there are defined 2 custom marks:
* `unit_test` - this annonates the unit tests
* `integration_test` - this annonates the integrations tests


#### How to run tests
**NOTE**: some tests are disabled locally, as they would take too long to pass, and that's quite annoying.

```bash
# Run this in the /generator directory 
python3 -m pytest

# Or this
pytest
```


### Examples
```bash
# Stream batches of time series data to the console, each batch contains 2048 values
python3 py_series_gen.py --target console --generator time-series --batch-size 2048 --stream

# Generate a single batch of 1000 time series values to the console
python3 py_series_gen.py --target console --generator time-series --batch-size 1000

# Stream batches of 32 time series values to the `py-topic` Kafka topic which is present at localhost:9092
python3 py_series_gen.py --target kafka --generator time-series --batch-size 32 --bootstrap-server localhost --port 9092 --topic py-topic --stream

# Send batch of 10 time series values to http://localhost:8080/ via HTTP POST request
python3 py_series_gen.py --target http --endpoint http://localhost:8080/ --batch-size 10 --generator time-series
```

### Architecture
The generator is built with a modular architecture (see docs for more). The 3 main concepts are Publishers, Targets, and generator functions. Both Publishers, and Targers are generated dynamically from the CLI arguments by their respective factories. The generator functions are implemented for each supported publish target.

- Publish Targets: Handle the state for different data destinations
- Publishers: These are responsible for the actual data sending to the data destinations
- Generator Functions: Produce the actual data (e.g., time_series_generator)

### Extending
For adding new targets:
1. Create a new target class implementing the target interface
2. Register the new target in the factory
3. Add CLI support for the new target

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
