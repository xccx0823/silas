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

            # Filter unwanted attributes
            if key.startswith('_') or key == 'Meta':
                continue

            # The original key
            original_key = key

            # Parse a single column rule
            value = self._parse_single_column(key, original_key, prefix, _attribute, _annotations)

            env_dict.update({
                original_key: value
            })

        return env_dict

    def __init__(self):
        _g = self._get_envs()
        _g_sort = sorted(_g.items(), key=lambda item: item[0])
        g = SettingDict(_g_sort)
        super().__init__(g)

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
        # Filter unwanted attributes
        if key.startswith('_') or key == 'Meta':
            return

        # The class of the object
        _class = self.__class__
        # All properties of the class
        _attribute = _class.__dict__
        # A variable whose type is defined
        _annotations = _attribute.get('__annotations__', {})

        # The original key
        original_key = key

        # prefix
        prefix = self.Meta.__dict__.get('prefix')
        if prefix:
            self.get_env(key)

        # Parse a single column rule
        value = self._parse_single_column(key, original_key, prefix, _attribute, _annotations)

        # The default value
        return value

    def _parse_single_column(self, key, original_key, prefix, _attribute, _annotations):
        """ Parse a single column rule
        """

        # Default value
        default_value = _attribute.get(key)

        # EnvField
        env_field_obj = None
        if isinstance(default_value, Env):
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
        typ = _annotations.get(original_key) or str
        if typ:
            value = self.trans_env_type(original_key, value, typ)

        # Checking environment variables is mandatory
        if value is None and original_key not in _attribute:
            raise UnsetEnvError(f'No environment variables are configured `{key}`')

        # The default value
        value = value or default_value

        # Map
        if value is not None and env_field_obj and env_field_obj.mp:
            un_match_value = value if env_field_obj.un_match_mp else None
            value = env_field_obj.mp.get(value, un_match_value)

        return value


class Env:
    """ A class that adds functionality to defined class attributes
    """

    def __init__(self, value=None, mp: dict = None, use_prefix: bool = False, un_match_mp=True):
        """ ~class.EnvField.obj

        :param value: Default value when environment variables are not set
        :param mp: Value Map
        :param use_prefix: Whether to use prefix. the default is False
        :param un_match_mp: Whether to fill in the original value when no data is matched
        """
        self.value = value
        self.mp = mp
        self.use_prefix = use_prefix
        self.un_match_mp = un_match_mp
