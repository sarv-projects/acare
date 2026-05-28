from setuptools import setup


package_name = "acare_planner"


setup(
    name=package_name,
    version="0.1.0",
    package_dir={package_name: "."},
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
    ],
    install_requires=["setuptools", "pydantic>=2.6", "numpy>=1.24", "PyYAML>=6.0"],
    zip_safe=True,
    maintainer="acare",
    maintainer_email="acare@todo.todo",
    description="ACARE ROS2 planner package",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "state_manager = acare_planner.state_manager:main",
            "planner_node = acare_planner.planner_node:main",
        ],
    },
)
