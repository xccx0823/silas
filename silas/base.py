# sys
import os
import json
from datetime import date, datetime

# project
from .error import UnrealizedError, TypeTransError


class SettingDict(dict):
    """ setting dict
    """

    def __init__(self, dic):
        dic = sorted(dic.items(), key=lambda item: item[0])
        super().__init__(dic)

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def __repr__(self):
        print_msg = 'Config:\n'
        for key, value in self.items():
            json_value = json.dumps(value, indent=4, sort_keys=True)
            single = f"\n>> {key}: {json_value}\n"
            print_msg += single
        return print_msg


class SettingBase:
    """ config basic class
    """

    def __init__(self, g):
        self.g: SettingDict = g

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
            if typ is datetime:
                fmt = self.Meta.__dict__.get('date_fmt')
                if isinstance(fmt, str):
                    fmt_str = fmt
                elif isinstance(fmt, dict):
                    fmt_str = fmt.get(key, '%Y-%m-%d %H:%M:%S')
                else:
                    fmt_str = '%Y-%m-%d %H:%M:%S'
                value = datetime.strptime(value, fmt_str)
            elif typ is date:
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

    def _meta_get(self, key):
        """ class.Meta.__dict__
        """
        return self.Meta.__dict__.get(key)

    def _cls_custom_config(self):
        """ Gets all custom class properties
        """
        config = dict(
            filter(
                lambda x: not x[0].startswith('_') and x[0] != 'Meta',
                self.__class__.__dict__.items()
            )
        )
        return config
