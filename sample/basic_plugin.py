import tkinter.messagebox

from abc import ABC

from pyvoxelhorizon.plugin import Plugin

PLUGIN_NAME = "BasicPlugin"


class BasicPlugin(Plugin, ABC):
    def on_create(self):
        pass

    def on_destroy(self):
        pass

    def on_update(self):
        pass

    def on_command(self, command) -> bool:
        if command == "test":
            tkinter.messagebox.showinfo("BasicPlugin", "Test Command..!")

            return True

        return False
