"""Json location"""
from models.engine.filestorage import FileStorage

location: str = 'tests/json/'
storage = FileStorage(location)
