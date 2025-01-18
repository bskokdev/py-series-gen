## What are targets in the context of this project?

- Target wraps all the relevant CLI arguments for a publisher to be able to produce data
    - These could be the generic arguments such as `batch_size`, `is_stream`, or other platform specific ones
- Target basically defines where, and how the generated data should be published to the desired destination
- Targets are produced dynamically within the application based on the CLI argument `--target <TARGET>`

#### Currently supported publish targets:
- Console

(Kafka coming soon)