from setuptools import setup, find_packages
import os

package_name = 'acare_vision'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='acare',
    maintainer_email='acare@todo.todo',
    description='ACARE vision',
    license='TODO',
    entry_points={
        'console_scripts': [
            'vision_node = vision_node:main',
        ],
    },
)
