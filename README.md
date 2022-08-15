# Silas

面向各式各样的配置文件获取配置

## 如何使用

```python
from datetime import date
from silas.env import EnvConfig, EnvField


class MySetting(EnvConfig):
    begin_date = EnvField(typ=date, default='1990-01-01', use_prefix=True)
    port = EnvField(typ=int, default=8081, use_prefix=False)

    class Meta:
        prefix = 'test'


```