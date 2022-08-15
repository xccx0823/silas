# project
from .base import SettingBase


class YmlConfig(SettingBase):
    """ Load the class configured by the YAML file
    """

    class Meta:
        file_path: str
