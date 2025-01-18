from . import Target


class ConsoleTarget(Target):
    """Class specific to the console publish destination (simple stdout)

    Args:
        Target: base class containing base arguments, and state
    """

    def __init__(self, batch_size: int = 0, is_stream: bool = False):
        super().__init__(batch_size=batch_size, is_stream=is_stream)

    def _validate_arguments(self):
        # Arguments are the same as for the generic target, no need for validation here
        pass
