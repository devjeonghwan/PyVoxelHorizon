class GameHook:
    address     : int       = None

    def __init__(self, address):
        self.address = address


    def on_start_scene(self, vh_controller_address: int, network_layer_address: int, plugin_path: str):
        return

    def on_run(self):
        return

    def on_destory_scene(self):
        return


    def on_mouse_left_button_down(self, x: int, y: int, flags: int):
        return

    def on_mouse_left_button_up(self, x: int, y: int, flags: int):
        return

    def on_mouse_right_button_down(self, x: int, y: int, flags: int):
        return

    def on_mouse_right_button_up(self, x: int, y: int, flags: int):
        return

    def on_mouse_move(self, x: int, y: int, flags: int):
        return

    def on_mouse_move_hv(self, move_x: int, move_y: int, left_button_pressed: bool, right_button_pressed: bool, middle_button_pressed: bool):
        return

    def on_mouse_wheel(self, wheel: int):
        return
    
    
    def on_console_command(self, command: str):
        return
    

    def on_key_down(self, key: int):
        return
    
    def on_key_up(self, key: int):
        return
    
    def on_key_down_func(self, key: int):
        return
    
    def on_key_down_control_func(self, key: int):
        return
    
    def on_key_down_func(self, key: int):
        return
    
    def on_character_unicode(self, key: int):
        return
    
    
    def on_pad_left_bumper_press(self):
        return
    
    def on_pad_left_bumper_release(self):
        return

    def on_pad_right_bumper_press(self):
        return
    
    def on_pad_right_bumper_release(self):
        return
    
    def on_pad_up_press(self):
        return
    
    def on_pad_up_release(self):
        return
    
    def on_pad_down_press(self):
        return
    
    def on_pad_down_release(self):
        return

    def on_pad_left_press(self):
        return
    
    def on_pad_left_release(self):
        return
    
    def on_pad_right_press(self):
        return
    
    def on_pad_right_release(self):
        return
    
    def on_pad_a_press(self):
        return
    
    def on_pad_a_release(self):
        return
    
    def on_pad_b_press(self):
        return
    
    def on_pad_b_release(self):
        return
    
    def on_pad_x_press(self):
        return
    
    def on_pad_x_release(self):
        return

    def on_pad_y_press(self):
        return
    
    def on_pad_y_release(self):
        return