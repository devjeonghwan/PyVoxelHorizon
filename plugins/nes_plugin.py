from voxel_horizon_plugin import VoxelHorizonPlugin
from pyvoxelhorizon.game.object import *
from pyvoxelhorizon.game.helper import VoxelEditor

from nes_py import NESEnv

import random
import math
import time
import numpy
import cv2

PLUGIN_NAME     = "NESPlugin"

TARGET_X        = 0
TARGET_Y        = 0
TARGET_Z        = 0

WIDTH = 100
HEIGHT = 100
FRAME_RATE = 12.0

class NESPlugin(VoxelHorizonPlugin):
    def on_initialize(self, game_context: GameContext):
        self.initialized = False

        self.nes_env = None
        self.nes_keys = None
        
        self.start_time = time.time()
        self.last_index = None

    def on_update(self, game_context: GameContext):
        battle_scene = game_context.get_battle_scene()

        if not battle_scene:
            return
        
        voxel_object_manager = battle_scene.get_voxel_object_manager()

        if not voxel_object_manager:
            return
        
        voxel_editor = VoxelEditor(voxel_object_manager)
        
        if self.nes_env:
            if not self.initialized:
                for w in range(WIDTH):
                    for h in range(HEIGHT):
                        _x = int(TARGET_X + (w * 50))
                        _y = int(TARGET_Y + (h * 50))
                        _z = int(TARGET_Z)
        
                        voxel_editor.add_voxel(_x, _y, _z, get_voxel_color(0))
                self.initialized = True

                return
            
            index = int((time.time() - self.start_time) * FRAME_RATE)

            if self.last_index != index:
                self.last_index = index

                action = self.nes_keys.get(None, 0)
                
                state, reward, done, info = self.nes_env.step(action)

                resized = cv2.resize(state, dsize=(WIDTH, HEIGHT), interpolation=cv2.INTER_CUBIC)
                frame = numpy.rot90(resized, -1, axes=(0, 1))

                for w in range(WIDTH):
                    for h in range(HEIGHT):
                        pixel = frame[w, h, :]

                        _x = int(TARGET_X + (w * 50))
                        _y = int(TARGET_Y + (h * 50))
                        _z = int(TARGET_Z)
        
                        voxel_editor.set_voxel_color(_x, _y, _z, find_similar_voxel_color(pixel[0], pixel[1], pixel[2]))
                        # voxel_editor.set_voxel_color(_x, _y, _z, get_voxel_color(0))
        voxel_editor.finish()
            
    def on_mouse_right_click(self, game_context: GameContext):
        if not self.nes_env:
            self.nes_env = NESEnv(self.get_path("super-mario-bros-1.nes"))
            self.nes_keys = self.nes_env.get_keys_to_action()

            state = self.nes_env.reset()

            game_context.write_text(0xffff0000, "Start ROM..!\n")
        else:
            self.nes_env.close()
            self.nes_env = None
            game_context.write_text(0xffff0000, "Stop ROM..!\n")

    def on_stop(self):
        return None
