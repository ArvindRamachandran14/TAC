# mainTest.py

import asyncio
from datetime import datetime

async def main() : 
	deltaT = 2						# seconds
	start = datetime.now()
	while True :
		now = datetime.now()
		diff = now - start
		ms = diff.seconds * 1000 + diff.microseconds / 1000
		print('Interval: {0:.1f}'.format(ms))
		start = now
		

		await asyncio.sleep(deltaT)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()


