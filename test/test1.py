import os
from silas.env import Env, EnvConfig


class MyEnvConfig(EnvConfig):
    """ test 1 class
    """
    name: str = Env('xc', mp={'x': 'father'}, use_prefix=False, un_match_mp=True)
    age: int = Env(19, use_prefix=False)
    ID = 1
    sex: str

    class Meta:
        prefix = 'auth_'


os.environ["auth_name"] = '123'
os.environ["auth_sex"] = '1'

config = MyEnvConfig()
print(config.g)

name = config.present_get('sex')
print(name)
