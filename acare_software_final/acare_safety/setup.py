from setuptools import setup


package_name = "acare_safety"


setup(
    name=package_name,
    version="0.1.0",
    package_dir={package_name: "."},
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="acare",
    maintainer_email="acare@todo.todo",
    description="ACARE ROS2 safety package",
    license="TODO",
    entry_points={
        "console_scripts": [
            "safety_node = acare_safety.safety_node:main",
        ],
    },
)
