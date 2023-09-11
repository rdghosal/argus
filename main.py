import datetime
import logging
import time

import asyncio
from apscheduler.schedulers import background
from apscheduler.schedulers import blocking
from websockets import server

from clients import PyPIClient
from parser import RequirementsParser


logging.basicConfig()
logging.getLogger("apscheduler").setLevel(logging.DEBUG)


EventLog = list()
pkg_registry = dict()


b = background.BackgroundScheduler()
p = RequirementsParser("./requirements.txt")


def get_pkg_versions() -> None:
    EventLog.append(datetime.datetime.utcnow())
    for requirement in p.parse():
        pkg_registry[requirement] = PyPIClient.get_latest_version(requirement)


async def echo(websocket):
    time.sleep(1)
    await websocket.send(f'{EventLog=}')


async def main():
    print('* starting')
    async with server.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    b.add_job(get_pkg_versions, "interval", seconds=3)
    b.start()
    asyncio.run(main())
