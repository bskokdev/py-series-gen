from argparse import Namespace, ArgumentParser
from collections import defaultdict
from typing import Tuple

from publishers.targets import TargetType

target_arg_to_type = defaultdict(None, {
    'console': TargetType.console,
    'kafka': TargetType.kafka
})

def get_args() -> Tuple[ArgumentParser, Namespace]:
    """Function which handles argument reading, and parsing.
    It produces the arguments namescape from which the parameters can be read.

    Returns:
        Namespace: An object from which we can access the parameters
    """
    parser = ArgumentParser()
    parser.add_argument('--target', dest='target', type=str)
    parser.add_argument('--batch-size', dest='batch_size', type=int)
    # This flag will cause the publisher to repeatedly send the batch to the target
    parser.add_argument('--stream', dest='stream', action='store_true', default=False)
    return (parser, parser.parse_args())