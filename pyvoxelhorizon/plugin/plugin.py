from abc import *

from pyvoxelhorizon.plugin.game import *
from pyvoxelhorizon.plugin.type import *


class Plugin(metaclass=ABCMeta):
    game: Game
    directory_path: str

    def __init__(self, game: Game, directory_path: str):
        self.game = game
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

    def on_command(self, command: str) -> bool:
        return False

    def on_mouse_click(self, x: int, y: int, button_type: MouseButtonType, pressed: bool) -> bool:
        return False

    def on_mouse_move(self, x: int, y: int) -> bool:
        return False

    def on_mouse_wheel(self, x: int, y: int, wheel: int) -> bool:
        return False

    def on_key(self, key_type: KeyType, pressed: bool) -> bool:
        return False

    def on_pad(self, button_type: PadButtonType, pressed: bool) -> bool:
        return False
