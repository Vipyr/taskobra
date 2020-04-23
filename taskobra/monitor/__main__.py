
import asyncio 
import argparse 
import psutil

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    return parser.parse_args()

async def cpu_monitoring(args):
    while True:
        await asyncio.sleep(5)
        print(f"CPU     : {psutil.cpu_percent()}")

async def memory_monitoring(args):
    while True:
        await asyncio.sleep(5)
        print(f"VMem    : {psutil.virtual_memory()}")
        print(f"SwapMem : {psutil.swap_memory()}")

async def disk_monitoring(args):
    while True:
        await asyncio.sleep(5)
        print(f"Disk    : {psutil.disk_usage('/')}")


if __name__ == "__main__":
    args = parse_args()
    loop = asyncio.get_event_loop()
    try:
        # TODO: If we deprecate pre-3.7 we can make this create_task
        task = asyncio.ensure_future(cpu_monitoring(args)) 
        task = asyncio.ensure_future(memory_monitoring(args)) 
        task = asyncio.ensure_future(disk_monitoring(args)) 
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
