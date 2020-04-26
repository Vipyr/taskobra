import argparse 
import psutil


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    return parser.parse_args()

def main(args):
    while True:
        # Create SnapShot()
        # Call Each function, have each return a metric 
        print(f"Disk    : {psutil.disk_usage('/')}")
        print(f"VMem    : {psutil.virtual_memory()}")
        print(f"SwapMem : {psutil.swap_memory()}")
        print(f"CPU     : {psutil.cpu_percent()}")
        # snapshot = for each metric snapshot.add(metric) 
        # with db connection of some sort 
            # db of some sort.commit(snapshot)


if __name__ == "__main__":
    args = parse_args()
    try:
        main(args)
    except KeyboardInterrupt:
        pass
    # TODO: Add handlers for SIGINT, SIGKILL, SIGABORT, SIGTERM
