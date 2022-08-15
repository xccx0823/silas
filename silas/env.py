# project
from .base import SettingBase, SettingDict
from .error import UnsetEnvError


class EnvConfig(SettingBase):
    """ The environment variable
    """

    class Meta:
        # prefix: Environment variable prefix; If 'prefix = 'ENV' is set,
        # the key of the environment variable is prefixed, This is what
        # it looks like: 'ENV_KEY'.
        prefix: str

    def _get_envs(self) -> dict:
        """ Get all the environment variables in the class
        """
        # The class of the object
        _class = self.__class__
        # All properties of the class
        _attribute = _class.__dict__
        # A variable whose type is defined
        _annotations = _attribute.get('__annotations__', {})

        # prefix
        prefix = self.Meta.__dict__.get('prefix')

        env_dict = {}
        for key in set(_attribute) | set(_annotations):
            # The original key
            original_key = key

            # Default value
            default_value = _attribute.get(key)

            # Filter unwanted attributes
            if key.startswith('_') or key == 'Meta':
                continue

            # EnvField
            if isinstance(default_value, EnvField):
                env_field_obj = default_value
                default_value = env_field_obj.value
                if env_field_obj.use_prefix and prefix:
                    key = prefix + key
            else:
                # Add a prefix
                if prefix:
                    key = prefix + key

            # Getting environment variables
            value = self.get_env(key)

            # Conversion type
            typ = _annotations.get(original_key)
            if typ:
                value = self.trans_env_type(original_key, value, typ)

            # Checking environment variables is mandatory
            if value is None and default_value is None:
                raise UnsetEnvError(f'No environment variables are configured `{key}`')

            # The default value
            value = value or default_value

            env_dict.update({
                original_key: value
            })

        return env_dict

    def __init__(self):
        if not self.g:
            self.g = SettingDict(self._get_envs())
        super().__init__()

    def refresh(self, key):
        """ Getting environment variables
        """
        value = self.get_env(key)
        if not value:
            raise UnsetEnvError(f'No environment variables are configured `{key}`')
        self.g[key] = value

    def present_get(self, key):
        """ Gets the current latest value
        """
        typ = self.__class__.__annotations__.get(key)
        default_value = self.__class__.__dict__.get(key)
        prefix = self.Meta.prefix
        if prefix:
            self.get_env(key)


class EnvField:
    """ A class that adds functionality to defined class attributes
    """

    def __init__(self, value=None, use_prefix=False):
        """ ~class.EnvField.obj

        :param value: Default value when environment variables are not set
        :param use_prefix: Whether to use prefix. the default is False
        """
        self.value = value
        self.use_prefix = use_prefix


class EnvMap:
    """ Adds a mapped class to a defined class attribute
    """

    def __init__(self, mp=None, use_prefix=False):
        """ ~class.EnvMap.obj

        :param mp: Value Map
        :param use_prefix: Whether to use prefix. the default is False
        """
        self.mp = mp
        self.use_prefix = use_prefix
