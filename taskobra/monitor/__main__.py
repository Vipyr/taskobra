import argparse
import datetime
import logging
import os
import psutil
import sys
import time
import platform 

from taskobra.orm import CpuPercent, get_engine, get_session, Snapshot
from taskobra.monitor import system_info


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v",  "--verbose",           action="store_true",  help="Increase output verbosity")
    parser.add_argument("-s",  "--sample-rate",       nargs="?", default=2.0, help="Database URI to connect to, defaults to localhost or using the DATABASE_URI environment variable")
    parser.add_argument("-d",  "--database-uri",      nargs="?",            help="Database URI to connect to, defaults to localhost or using the DATABASE_URI environment variable")
    parser.add_argument("-pw", "--database-password", nargs="?",            help="Database password to use in the URI, not used if the URI is specified")
    parser.add_argument("-u",  "--database-username", nargs="?",            help="Database username to use in the URI, not used if the URI is specified")
    return parser.parse_args()


def create_snapshot(args):
    snapshot = Snapshot(timestamp=datetime.datetime.now())
    # Call Each function, have each return a metric
    # print(f"Disk    : {psutil.disk_usage('/')}")
    # print(f"VMem    : {psutil.virtual_memory()}")
    # print(f"SwapMem : {psutil.swap_memory()}")
    snapshot.metrics.append(CpuPercent(core_id=0, mean=psutil.cpu_percent()))
    # snapshot = for each metric snapshot.add(metric)
    return snapshot

def create_database_engine(args):
    if args.database_uri:
        return get_engine(args.database_uri)

    if 'DATABASE_URI' in os.environ:
        print(f" * Connecting to database {os.environ.get('DATABASE_URI')}")
        return get_engine(os.environ.get('DATABASE_URI'))

    # If the fully resolved database URI is not provided, use the credentials and connect to localhost
    database_username = args.database_username if args.database_username else os.environ.get('POSTGRES_USER', None)
    database_password = args.database_password if args.database_password else os.environ.get('POSTGRES_PASSWORD', None)
    if (database_password is None) or (database_username is None):
        logging.error("Error when connecting to the database, database user or password not found.")
        sys.exit(1)
    else:
        database_uri = f"postgresql://{database_username}:{database_password}@127.0.0.1:5432/taskobra"
        print(f" * Connecting to database {database_uri}")
        return get_engine(database_uri)


def main(args):
    database_engine = create_database_engine(args)
    system_info.create_system(args, database_engine)
    while True:
        time.sleep(args.sample_rate)
        snapshot = create_snapshot(args)
        snapshot.sample_rate = args.sample_rate
        with get_session(bind=database_engine) as session:
            print(snapshot)
            session.add(snapshot)
            session.commit()


if __name__ == "__main__":
    args = parse_args()
    try:
        main(args)
    except KeyboardInterrupt:
        pass
    # TODO: Add handlers for SIGINT, SIGKILL, SIGABORT, SIGTERM
