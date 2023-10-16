from abc import *


class Plugin(metaclass=ABCMeta):
    directory_path: str = None

    def __init__(self, directory_path: str):
        self.directory_path = directory_path

    @abstractmethod
    def on_create(self):
        pass

    @abstractmethod
    def on_destroy(self):
        pass

    @abstractmethod
    def on_update(self):
        pass

    def on_command(self, command) -> bool:
        return False
