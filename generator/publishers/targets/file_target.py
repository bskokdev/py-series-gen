import os
from enum import Enum

from .target import Target


class FileType(Enum):
    CSV = 1


extension_to_filetype = {
    ".csv": FileType.CSV,
}


class FileTarget(Target):
    """Generic state object for various file targets. It contains only the core arguments,
    and file path.
    """

    def __init__(
        self,
        file_path: str = "",
        batch_size: int = 0,
        is_stream: bool = False,
    ):
        self.file_path = file_path
        super().__init__(batch_size=batch_size, is_stream=is_stream)
        self._determine_file_type()

    def _validate_arguments(self):
        """Validates base, and file specific arguments.

        Raises:
            ValueError: Raised if file path not provided or points to a directory.
                Path should exclusively point to an existing file.
        """
        super()._validate_arguments()
        if not self.file_path:
            raise ValueError("Valid file path has to be specified (--path FILE_PATH)")

        # NOTE: We don't care if the file already exists as it shall be created
        #   but we can't create such file in directory without knowing its name, and extension
        if os.path.isdir(self.file_path):
            raise ValueError(
                "Directory path is not supported, provide path to a file (~/dir/file.csv)"
            )

    def _determine_file_type(self):
        """Determines the file type based on the file path extension.
        "~/dir/file.csv" would resolve into FileType.CSV

        Raises:
            ValueError: Raised if the extension isn't backed by an existing file type
        """
        for extension, file_type in extension_to_filetype.items():
            if self.file_path.endswith(extension):
                self.file_type = file_type
                return

        raise ValueError("Not supported extension, or invalid file path was provided")
