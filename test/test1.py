import os
from silas.env import EnvField, EnvConfig


class MyEnvConfig(EnvConfig):
    """ test 1 class
    """
    name: str = 'silas'
    age: int = EnvField(19, use_prefix=False)
    ID = 1
    sex: int

    class Meta:
        prefix = 'auth_'


os.environ["auth_name"] = '123'
config = MyEnvConfig()
config.present_get('name')
