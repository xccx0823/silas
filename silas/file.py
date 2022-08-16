# project
from .base import SettingBase, SettingDict
from .error import NoPathError, UnrealizedError, VariableValueError
from .enumerate import FileType
from .files.yml import read_yaml_file


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
        _g = self._handling_default()
        g = SettingDict(_g)
        super().__init__(g)

    def _get_file_config(self):
        """ Gets the specified configuration file
        """
        # If an environment variable is configured, it gets the
        # address specified by the environment variable
        file_env = self._meta_get('file_env')
        if file_env:
            path = self.get_env(file_env)
        else:
            path = None

        # If an environment variable is set but there is no address,
        # the file address set by the 'file_path' variable is used
        file_path = self._meta_get('file_path')
        path = path or file_path

        # Check whether the address is configured
        if not path:
            raise NoPathError('No address is configured. please set the configuration `file_env` or `file_path`.')

        # Get the type of the configuration file
        file_type = self._meta_get('file_type')

        if not file_type:
            raise VariableValueError('`file_type` must be set in the Meta class')

        # Different configuration file parsing logic
        # is performed depending on the file type
        if file_type in (FileType.yml, FileType.yaml):
            config = read_yaml_file(path)
        else:
            raise UnrealizedError('Parsing logic for this configuration file is not implemented')

        return config

    def _handling_default(self) -> dict:
        """ Handling default configurations

        - Configurations that are defined in the class,
          but not in the configuration file, are populated in 'g'
        - For those defined in both the class and configuration,
          the default configuration in the class is overridden in
          the configuration file
        """
        # Gets the configuration in all classes
        config = self._cls_custom_config()

        # Get the configuration in the configuration file
        file_config = self._get_file_config()

        # Replace the configuration
        config.update(file_config)

        return config
