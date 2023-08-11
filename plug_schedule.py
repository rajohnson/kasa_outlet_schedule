import asyncio
import logging
import datetime

import kasa

from config import ip_address  # config just declares ip_address as a string

DAY_START_HOUR = 9
DAY_END_HOUR = 19

DAY_ON_TIME_S = 14
DAY_OFF_TIME_S = 0.7 * 60

NIGHT_ON_TIME_S = 10
NIGHT_OFF_TIME_S = 1.4 * 60

RETRY_DELAY_S = 5


async def main() -> None:
    device = kasa.SmartStrip(ip_address)
    while True:
        if DAY_START_HOUR <= datetime.datetime.now().hour < DAY_END_HOUR:
            ON_TIME_S = DAY_ON_TIME_S
            OFF_TIME_S = DAY_OFF_TIME_S
        else:
            ON_TIME_S = NIGHT_ON_TIME_S
            OFF_TIME_S = NIGHT_OFF_TIME_S
        try:
            logging.info("Turning on")
            await device.turn_on()
            logging.info(f"Waiting for {ON_TIME_S} seconds")
            await asyncio.sleep(ON_TIME_S)
            logging.info("Turning off")
            await device.turn_off()
            logging.info(f"Waiting for {OFF_TIME_S} seconds")
            await asyncio.sleep(OFF_TIME_S)
        except kasa.SmartDeviceException:
            logging.error("Device is unreachable")
            await asyncio.sleep(RETRY_DELAY_S)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(message)s",
        level=logging.DEBUG,
    )
    asyncio.run(main())
