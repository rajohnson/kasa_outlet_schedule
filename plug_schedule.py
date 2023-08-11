import asyncio
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
            await device.turn_on()
            await asyncio.sleep(ON_TIME_S)
            await device.turn_off()
            await asyncio.sleep(OFF_TIME_S)
        except kasa.SmartDeviceException:
            print("Device is unreachable")
            await asyncio.sleep(RETRY_DELAY_S)


if __name__ == "__main__":
    asyncio.run(main())
