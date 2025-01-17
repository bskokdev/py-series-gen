from argparse import ArgumentParser
from collections import defaultdict
from typing import List, Tuple

from publishers.targets import TargetFactory, TargetType, Target

# maps a target type argument string to an actual enum class, for better typing
target_arg_to_type = defaultdict(None, {
    'console': TargetType.console,
    'kafka': TargetType.kafka
})

# maps a target type to a list of arguments specific to such type
specific_target_args = defaultdict(None, {
    # TargetType.console: [
    #     ('--console-test', 'console_test', int),
    # ]
})

def _attach_target_args(parser: ArgumentParser, specific_args_list: List[Tuple]):
    for argument, variable, dtype in specific_args_list:
        parser.add_argument(argument, dest=variable, type=dtype)
    

def build_target_from_args() -> Target:
    """Constructs a publish target object. This function also allows for dynamic argument attachment,
    based on the type of the publish target. 

    Returns:
        Target: A publish target constructed based on the type, and CLI arguments
    """
    parser = ArgumentParser()
    parser.add_argument('--target', dest='target', type=str)
    parser.add_argument('--batch-size', dest='batch_size', type=int)
    parser.add_argument('--stream', dest='is_stream', action='store_true', default=False)
    
    temp_args, _ = parser.parse_known_args() # only used to access the target argument

    target_type = target_arg_to_type[temp_args.target]
    if target_type in specific_target_args:
        _attach_target_args(parser, specific_target_args[target_type])
    
    final_args = parser.parse_args()
    return TargetFactory().create_target(target_type=target_type, args=final_args)