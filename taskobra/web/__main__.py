import os
import sys

from . import create_app
from tests.utils.TestDatabase import TestDatabase
from tests.utils.data_generators import fake_systems_generator


if __name__ == "__main__":
    """
    Test entry point for the web application
        Note: Running in this mode is _not_ recommended for Production Environments
        Debug for the WSGI Werkzeug server is turned ON, which will expose you to remote attacks
        Only ever use this with localhost and test environments!
    """
    with TestDatabase(f"sqlite:////tmp/taskobra.{os.getpid()}.sqlite.db", fake_systems_generator(20)):
        app = create_app()
        app.run(host='localhost', debug=True)
