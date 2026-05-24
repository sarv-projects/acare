from setuptools import find_packages
from setuptools import setup

setup(
    name='acare_msgs',
    version='0.0.0',
    packages=find_packages(
        include=('acare_msgs', 'acare_msgs.*')),
)
