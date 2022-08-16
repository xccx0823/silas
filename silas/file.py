# project
from .base import SettingBase
from .error import NoPathError, UnrealizedError, VariableValueError
from .enumerate import FileType
from silas.files.yml import read_yaml_file


class FileConfig(SettingBase):
    """ Load the class configured by the file
    """

    class Meta:
        # If the 'file_env' configuration is specified,
        # the 'file_path' configuration is overridden
        file_env: str
        file_path: str
        file_type: FileType

    def __init__(self):
        g = self._get_file()
        super().__init__(g)

    def _get_file(self):
        """ Gets the specified configuration file
        """
        # If an environment variable is configured, it gets the
        # address specified by the environment variable
        file_env = self._meta_get('file_env')
        path = self._meta_get('file_path')
        if file_env:
            path = self.get_env(file_env)

        # Check whether the address is configured
        if not path:
            raise NoPathError('No address is configured.')

        # Get the type of the configuration file
        file_type = self._meta_get('file_type')

        if not file_type:
            VariableValueError('`file_type` must be set in the Meta class')

        # Different configuration file parsing logic
        # is performed depending on the file type
        if file_type in (FileType.yml, FileType.yaml):
            config = read_yaml_file(path)
        else:
            raise UnrealizedError('Parsing logic for this configuration file is not implemented')

        return config
