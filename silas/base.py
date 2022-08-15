# sys
import os
from datetime import date, datetime

# project
from .error import UnrealizedError, TypeTransError


class SettingDict(dict):
    """ setting dict
    """

    def __init__(self, dic: dict):
        super().__init__(dic)

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value


class SettingBase:
    """ config basic class
    """

    g: SettingDict = {}

    class Meta:
        # Date formatting
        date_fmt: str

    def present_get(self, key):
        """ Gets the current latest value
        """
        raise UnrealizedError(' The specified method `present_get` is not implemented')

    def refresh(self, key):
        """ Refresh the value
        """
        raise UnrealizedError(' The specified method `refresh` is not implemented')

    @staticmethod
    def get_env(key):
        """ Getting environment variables
        """
        return os.environ.get(key)

    def trans_env_type(self, key, value, typ):
        """ Converts the type of an environment variable value
        """
        if value is None:
            return value

        try:
            if isinstance(typ, datetime):
                fmt = self.Meta.__dict__.get('date_fmt')
                if isinstance(fmt, str):
                    fmt_str = fmt
                elif isinstance(fmt, dict):
                    fmt_str = fmt.get(key, '%Y-%m-%d %H:%M:%S')
                else:
                    fmt_str = '%Y-%m-%d %H:%M:%S'
                value = datetime.strptime(value, fmt_str)
            elif isinstance(typ, date):
                fmt = self.Meta.__dict__.get('date_fmt')
                if isinstance(fmt, str):
                    fmt_str = fmt
                elif isinstance(fmt, dict):
                    fmt_str = fmt.get(key, '%Y-%m-%d')
                else:
                    fmt_str = '%Y-%m-%d'
                value = datetime.strptime(value, fmt_str)
            else:
                value = typ(value)
        except Exception as e:
            raise TypeTransError(e)

        return value
