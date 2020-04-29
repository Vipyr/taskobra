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
        "flask_sqlalchemy",
        "psutil",
        "psycopg2",
        "sqlalchemy",
        "py-cpuinfo",
    ],
)
