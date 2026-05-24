from setuptools import setup, find_packages
import os

package_name = 'acare_voice'

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
    description='ACARE voice pipeline',
    license='TODO',
    entry_points={
        'console_scripts': [
            'voice_ros_node = voice.voice_ros_node:main',
        ],
    },
)
