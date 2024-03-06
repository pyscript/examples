from files import *
from pyscript import window, display
import media

my_files = Files()

async def get_file(event):
    data = await my_files.get_file_contents("test.txt")
    display(data)

await media.list_media_devices()