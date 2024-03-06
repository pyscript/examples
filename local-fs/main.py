from files import *
from pyscript import window

my_files = Files()

async def get_file(event):
    data = await my_files.get_file_contents("test.txt")
    window.console.log(data)