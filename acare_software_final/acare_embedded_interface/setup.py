from setuptools import setup


package_name = "acare_embedded_interface"


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
    description="ACARE embedded interface node",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "interface_node = acare_embedded_interface.embedded_interface_node:main",
        ],
    },
)
