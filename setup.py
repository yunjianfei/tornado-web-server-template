from setuptools import find_packages
#from setuptools import setup, find_packages
from distutils.core import setup
import sys,os

VERSION = '1.0'
PACKAGE = "tor_manager"
NAME = "tor_manager"
DESCRIPTION = ""
AUTHOR = "YunJianFei"
AUTHOR_EMAIL = "jianfeiyun@gmail.com"
URL = ""
long_description = ""

setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = long_description,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    license = "Linux",
    url = URL,
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        'tornado>=3.0',
    ],
    py_modules  = ['manager'],
    entry_points = {
        'console_scripts': [
            'tor_manager = manager:main',
        ],
    },
)
