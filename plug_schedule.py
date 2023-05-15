import asyncio
import kasa
from config import ip_address  # config just declares ip_address as a string

ON_TIME_S = 2
OFF_TIME_S = 8
RETRY_DELAY_S = 1


async def main() -> None:
    device = kasa.SmartStrip(ip_address)
    while True:
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
