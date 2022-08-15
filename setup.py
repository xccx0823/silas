# sys
import re

# 3p
from setuptools import setup, find_packages


def read(path):
    with open(path, 'r', encoding='utf8') as fp:
        content = fp.read()
    return content


def find_version(path):
    match = re.search(r'__version__ = [\'"](?P<version>[^\'"]*)[\'"]', read(path))
    if match:
        return match.group('version')
    raise RuntimeError("Cannot find version information")


setup(
    name='silas',
    version=find_version('silas/__init__.py'),
    author='XChao',
    author_email='cheerxiong0823@163.com',
    description='Fast and convenient configuration reading.',
    long_description='README.md',
    url='https://github.com/xccx0823/silas',
    packages=find_packages(),
    include_package_data=True,
    install_requires=read('requirements.txt').splitlines(),
    python_requires=">=3.6",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
