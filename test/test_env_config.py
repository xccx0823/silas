import os
from datetime import datetime

from silas.env import Env, EnvConfig


class MyEnvConfig(EnvConfig):
    """ test 1 class
    """
    name: str = Env('human', mp={'human': 'xc', 'animal': 'pig'}, use_prefix=True, un_match_mp=True)
    age: int = Env(19, use_prefix=False)
    ID = 1
    sex: str
    begin_date: datetime

    class Meta:
        prefix = 'auth_'


os.environ["auth_name"] = '123'
os.environ["age"] = '20'
os.environ["auth_sex"] = '男'
os.environ["auth_begin_date"] = '2020-01-01 00:00:00'

config = MyEnvConfig()
print(config.g)

os.environ["auth_sex"] = '无性别'
sex = config.present_get('sex')
print(config.g.sex)
print(sex)

begin_date = config.present_get('begin_date')
print(begin_date)
