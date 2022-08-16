# sys
import os

# 3p
import yaml

# project
from silas.error import NoPathError, FileParseError, FileTypeError


def read_yaml_file(path):
    """ Read the YAML file
    """

    # Check the file exists
    if not os.path.exists(path):
        raise NoPathError(f'Not found: `{path}`')

    # Check file types
    if not path.endswith('.yaml') or path.endswith('.yml'):
        FileTypeError(f'{path} is not a YAML file')

    with open(path, 'r', encoding='utf-8') as stream:
        try:
            yaml_config = yaml.load(stream, Loader=yaml.SafeLoader)
        except Exception as e:
            raise FileParseError(e)
    return yaml_config
