import os
from datetime import datetime

from silas.env import Env, EnvConfig


class MyEnvConfig(EnvConfig):
    """ test 1 class
    """
    name: str = Env('xc', mp={'x': 'father'}, use_prefix=False, un_match_mp=True)
    age: int = Env(19, use_prefix=False)
    ID = 1
    sex: str
    begin_date: datetime

    class Meta:
        prefix = 'auth_'


os.environ["auth_name"] = '123'
os.environ["auth_sex"] = '1'
os.environ["auth_begin_date"] = '2020-01-01 00:00:00'

config = MyEnvConfig()
print(config.g)

sex = config.present_get('sex')
print(sex)

begin_date = config.present_get('begin_date')
print(begin_date)
