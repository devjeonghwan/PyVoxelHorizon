from voxel_horizon_plugin import VoxelHorizonPlugin
from pyvoxelhorizon.game.object import *
from pyvoxelhorizon.game.helper import VoxelEditor

import random
import math

PLUGIN_NAME     = "TestPlugin"
SIZE = 50
INTERVAL = 5

class TestPlugin(VoxelHorizonPlugin):
    def on_initialize(self, game_context: GameContext):
        self.is_playing = False
        self.last_wave = 0
        self.current_index = 0

    def on_update(self, game_context: GameContext):
        battle_scene = game_context.get_battle_scene()

        if not battle_scene:
            return
        
        voxel_object_manager = battle_scene.get_voxel_object_manager()

        if not voxel_object_manager:
            return
        
        if self.is_playing:
            self.current_index += 1

            if self.current_index % INTERVAL != 0:
                return
            
            voxel_editor = VoxelEditor(voxel_object_manager)
            PI_VOL = 4
            for x in range(SIZE):
                y_value = (math.sin(x / 2 + self.last_wave) + 1) * PI_VOL

                _x = 200 + (x * 50)
                _y = -200 + (y_value * 50)
                _z = 200

                voxel_editor.remove_voxel(_x, _y, _z)

            self.last_wave = self.last_wave + 0.5

            for x in range(SIZE):
                y_value = (math.sin(x / 2 + self.last_wave) + 1) * PI_VOL

                _x = 200 + (x * 50)
                _y = -200 + (y_value * 50)
                _z = 200

                voxel_editor.add_voxel(_x, _y, _z, random.randint(0, 23))

            voxel_editor.finish()


    def on_mouse_right_click(self, game_context: GameContext):
        if not self.is_playing:
            self.is_playing = True
            game_context.write_text(0xffff0000, "Start Wave!\n")
        else:
            self.is_playing = False
            game_context.write_text(0xff00ff00, "Stop Wave!\n")

    def on_stop(self):
        return None
