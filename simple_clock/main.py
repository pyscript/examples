from datetime import datetime
from pyscript import display
import asyncio

def now():
    fmt = "%m/%d/%Y, %H:%M:%S"
    return f"{datetime.now():{fmt}}"

display(now(), target="output1", append=False)

async def foo():
    while True:
        await asyncio.sleep(1)
        output = now()
        display(output, target="output2", append=False)

        if output[-1] in ["0", "4", "8"]:
            display("It's espresso time!", target="output3", append=False)
        else:
            display("", target="output3", append=False)

await foo()
