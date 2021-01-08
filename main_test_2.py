
import asyncio

class TAC():

    def __init__(self):

        self.sem = asyncio.Semaphore(1)  


        self.bdone = False

    async def read_instruments(self):

        while not self.bdone:

            async with self.sem:

                print('Reading instruments')

            await asyncio.sleep(0.050)

    async def doCmd(self):

        try:

            while not self.bdone:

                async with self.sem:

                    print(2/0)

                    print("Processing command")

                await asyncio.sleep(0.050)

        except (ZeroDivisionError, RuntimeError, TypeError, NameError, KeyboardInterrupt) as e:

            self.Terminate()


    def Terminate(self):

        self.bdone = True

        print('Terminated')





async def main() :

    tac = TAC()

    task1 = asyncio.create_task(tac.read_instruments())

    task2 = asyncio.create_task(tac.doCmd())

    await task1

    await task2

asyncio.run(main())

'''
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
'''