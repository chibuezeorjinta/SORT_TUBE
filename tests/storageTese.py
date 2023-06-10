from models.engine.filestorage import FileStorage

location: str = 'tests/json/'
print(location)

storage = FileStorage(location)
storage.all()