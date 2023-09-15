from voxel_horizon_plugin import VoxelHorizonPlugin
import time

PLUGIN_NAME     = "BadApplePlugin"
FRAME_FORMAT    = "frames/%d.vxl"
FRAME_LENGTH    = 6568
FRAME_RATE      = 30.0

class BadApplePlugin(VoxelHorizonPlugin):
    def on_initialize(self, client_context):
        self.client_context = client_context
        
        self.start_time = None
        self.last_index = None
        self.playing = False

    def on_loop(self, game_object):
        # Scene
        scene_object = game_object.get_scene()

        if scene_object is not None and self.playing:
            # Calculate index using duration
            index = int((time.time() - self.start_time) * FRAME_RATE)

            if index < FRAME_LENGTH:
                # Check last index
                if self.last_index != index:
                    self.last_index = index

                    # Upload VXL files
                    scene_object.load_voxels(self.get_path(FRAME_FORMAT % index))
            else:
                self.last_index = None
                self.playing = False
        
        # Get last right mouse button status
        right_down = game_object.is_mouse_right_button_down()

        # Check if clicked
        if right_down != 0:
            # Show message
            self.show_message("Start Playing Bad Apple!")

            # Set flags to playing!
            self.start_time = time.time()
            self.playing = True
        
    def on_stop(self):
        return None
