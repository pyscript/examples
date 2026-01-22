from pyscript import window

class Files:
    def __init__(self):
        self.folder = None
        
    async def select_folder(self, event=None):
        self.folder = await window.showDirectoryPicker()

    async def get_file_contents(self, file_name):
        file = await self.folder.getFileHandle(file_name)
        file_data = await file.getFile()
        return await file_data.text()

    async def create_new_file(self, contents):
        file = await window.showSaveFilePicker()
        await self.write_file(file, contents)

    async def write_file(self, file, contents):
        writeable = await file.createWritable()
        await writeable.write(contents)
        await writeable.close()