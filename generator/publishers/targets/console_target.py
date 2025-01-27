from .target import Target


class ConsoleTarget(Target):
    """Implementation of the console target is identical to the abstract target.
    However, we use this class for better readability.
    """

    def _validate_arguments(self):
        # Arguments are the same as for the generic target, no need for validation here
        # We also have to implement this method otherwise we couldn't instantiate this class
        pass
