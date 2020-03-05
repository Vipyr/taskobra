from setuptools import setup

setup(
    name = "taskobra",
    packages = [
        "taskobra.orm",
    ],
    install_requires = [
        "sqlalchemy",
    ],
)
