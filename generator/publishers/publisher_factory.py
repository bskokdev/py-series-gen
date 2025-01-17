from . import ConsolePublisher, Publisher
from .targets import TargetType, Target


class PublisherFactory:
    """Factory class which constructs new publishers."""
    @staticmethod
    def create_publisher(generator_func: any, target: Target) -> Publisher:
        """The main factory method which takes in publish cli args,
        and a generator function and creates a new publisher based on these arguments.

        Args:
            target (Target): publish target to send the data to. This contains all the metadata to do that.
            generator_func (any): generator function which creates the data

        Raises:
            ValueError: ValueError is raised if arguments don't match the pattern matching cases

        Returns:
            Publisher: concrete publisher implementation
        """
        match target.type:
            case TargetType.console:
                return ConsolePublisher(generator_fun=generator_func, target=target)
            case _:
                raise ValueError('Target was not provided or no such target exists.')
        