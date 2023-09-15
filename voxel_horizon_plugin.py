from pyvoxelhorizon.game.object import *

import os
import tkinter.messagebox

class VoxelHorizonPlugin:
    working_directory               : str   = None

    last_mouse_left_down_state      : bool  = False
    last_mouse_right_down_state     : bool  = False

    def __init__(self, working_directory: str):
        self.working_directory = working_directory
    
    def update(self, game_context: GameContext):
        mouse_left_down_state = game_context.is_mouse_left_button_down()
        mouse_right_down_state = game_context.is_mouse_right_button_down()
        
        if mouse_left_down_state != self.last_mouse_left_down_state and mouse_left_down_state:
            self.on_mouse_left_click(game_context)
            
        if mouse_right_down_state != self.last_mouse_right_down_state and mouse_right_down_state:
            self.on_mouse_right_click(game_context)

        self.last_mouse_left_down_state = mouse_left_down_state
        self.last_mouse_right_down_state = mouse_right_down_state

        self.on_update(game_context)
        
    def on_initialize(self, game_context: GameContext):
        return None

    def on_update(self, game_context: GameContext):
        return None
        
    def on_mouse_left_click(self, game_context: GameContext):
        return None
    
    def on_mouse_right_click(self, game_context: GameContext):
        return None
    
    def on_stop(self):
        return None
    
    def get_path(self, path: str) -> str:
        return os.path.join(self.working_directory, path)

    def show_message(self, message: str):
        tkinter.messagebox.showinfo(title= str(self.__class__.__name__) + " Message", message=message)
