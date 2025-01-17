from .publisher import Publisher
from .console_publisher import ConsolePublisher
from .targets import TargetType
from cli.arguments import target_arg_to_type


class PublisherFactory():
    """Factory class which constructs new publishers."""
    @staticmethod
    def create_publisher(target_arg: str, is_stream_arg: bool, generator_func: any) -> Publisher:
        """The main factory method which takes in publish cli args,
        and a generator function and creates a new publisher based on these arguments.

        Args:
            target (str): publish target to send the data to
            is_stream (bool): should the batch be repeatedly be sent to the target
            generator_func (any): generator function which creates the data

        Raises:
            ValueError: ValueError is raised if arguments don't match the pattern matching cases

        Returns:
            Publisher: concrete publisher implementation
        """
        match target_arg_to_type[target_arg]:
            case TargetType.console:
                return ConsolePublisher(generator_fun=generator_func, is_stream=is_stream_arg)
            case _:
                raise ValueError('Target was not provided or no such target exists.')
        