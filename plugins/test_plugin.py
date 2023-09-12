from voxel_horizon_plugin import VoxelHorizonPlugin

PLUGIN_NAME     = "TestPlugin"

class TestPlugin(VoxelHorizonPlugin):
    def on_initialize(self, client_context):
        self.client_context = client_context

    def on_loop(self, game_object):
        # Scene
        scene_object = game_object.get_scene()

        if scene_object is not None:
            print("Scene..!")
            
        # Get last right mouse button status
        right_down = game_object.is_mouse_right_button_down()

        # Check if clicked
        if right_down != 0:
            # Show message
            self.show_message("Clicked!")
        
    def on_stop(self):
        return None
