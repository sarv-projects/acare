from setuptools import setup


package_name = "acare_bringup"


setup(
    name=package_name,
    version="0.1.0",
    package_dir={package_name: "."},
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/launch", ["launch/acare.launch.py"]),
        (
            f"share/{package_name}/config",
            [
                "config/system.yaml",
                "config/thresholds.yaml",
                "config/probability_map.yaml",
            ],
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="acare",
    maintainer_email="acare@todo.todo",
    description="ACARE ROS2 bringup and shared config",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "supervisor_node = acare_bringup.supervisor_node:main",
        ],
    },
)
