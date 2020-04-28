from setuptools import setup

setup(
    name = "taskobra",
    packages = [
        "taskobra.monitor",
        "taskobra.orm",
        "taskobra.web",
    ],
    install_requires = [
        "flask",
        "psutil",
        "psycopg2",
        "sqlalchemy",
    ],
)
