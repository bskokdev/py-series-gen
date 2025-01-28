from .target import Target


class ConsoleTarget(Target):
    """Implementation of the console target is identical to the abstract target.
    However, we use this class for better readability.
    """

    def _validate_arguments(self):
        return super()._validate_arguments()
