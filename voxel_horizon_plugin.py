import os
import tkinter.messagebox

class VoxelHorizonPlugin:
    def __init__(self, working_directory):
        self.working_directory = working_directory
    
    def on_initialize(self, client_context):
        return None

    def on_loop(self, game_object):
        return None
        
    def on_stop(self):
        return None
    
    def get_path(self, path):
        return os.path.join(self.working_directory, path)

    def show_message(self, message):
        tkinter.messagebox.showinfo(title= str(self.__class__.__name__) + " Message", message=message)
