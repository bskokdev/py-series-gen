## Information about testing 

There should be 2 kinds of tests present in the generator
- Unit tests for complex logical functionalities (such as chunk splitting the batches)
- Integration tests for each new PublishTarget
    - Whenever a new target and publisher are added, a new integration test should be added as well
    - This can probably be ignored for the ConsolePublisher, and ConsoleTarget as they don't have a real value

### How to run the tests

The library used for the testing is called `pytest`, so all that's required to run the tests is to run `pytest` command.
This will run both unit and integration tests (all files with the `test_*.py` or `*_test.py` pattern).

Why pytest? It has better syntax than `unittest`, uses plain asserts, and has support for fixtures which are handy in integration testing.