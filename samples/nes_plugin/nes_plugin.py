from voxel_horizon_plugin import VoxelHorizonPlugin
from pyvoxelhorizon.game.object import *
from pyvoxelhorizon.game.helper import VoxelEditor

from nes_py import NESEnv

import random
import math
import time
import numpy
import cv2

PLUGIN_NAME         = "NESPlugin"

TARGET_X            = 0
TARGET_Y            = 0
TARGET_Z            = 0

WIDTH               = 100
HEIGHT              = 100
FRAME_RATE          = 10.0
FRAME_RATE_INTERVAL = 1 / FRAME_RATE

class NESPlugin(VoxelHorizonPlugin):
    def on_initialize(self, game_context: GameContext):
        self.initialized = False

        self.nes_env = None
        self.nes_keys = None
        
        self.last_time = time.time()

    def on_update(self, game_context: GameContext):
        battle_scene = game_context.get_battle_scene()

        if not battle_scene:
            return
        
        voxel_object_manager = battle_scene.get_voxel_object_manager()

        if not voxel_object_manager:
            return
        
        voxel_editor = VoxelEditor(voxel_object_manager)
        
        if not self.initialized:
            for w in range(WIDTH):
                for h in range(HEIGHT):
                    _x = int(TARGET_X + (w * 50))
                    _y = int(TARGET_Y + (h * 50))
                    _z = int(TARGET_Z)
    
                    voxel_editor.add_voxel(_x, _y, _z, get_voxel_color(0))
            self.initialized = True

            return
        
        if self.nes_env:
            now = time.time()
            interval = now - self.last_time

            if interval > FRAME_RATE_INTERVAL:
                self.last_time = now

                key_list = []

                if game_context.is_key_press(KEY_A):
                    key_list.append(97)
                if game_context.is_key_press(KEY_W):
                    key_list.append(119)
                if game_context.is_key_press(KEY_S):
                    key_list.append(115)
                if game_context.is_key_press(KEY_D):
                    key_list.append(100)
                    
                if game_context.is_key_press(KEY_SPACE):
                    key_list.append(111)
                if game_context.is_key_press(KEY_RETURN):
                    key_list.append(112)

                if game_context.is_key_press(KEY_O):
                    key_list.append(32)
                if game_context.is_key_press(KEY_L):
                    key_list.append(13)
                
                action = self.nes_keys.get(tuple(key_list), 0)

                state, reward, done, info = self.nes_env.step(action)
                # Speed UP
                # for i in range(2):
                #     state, reward, done, info = self.nes_env.step(action)

                resized = cv2.resize(state, dsize=(WIDTH, HEIGHT), interpolation=cv2.INTER_CUBIC)
                frame = numpy.rot90(resized, -1, axes=(0, 1))

                for w in range(WIDTH):
                    for h in range(HEIGHT):
                        pixel = frame[w, h, :]

                        _x = int(TARGET_X + (w * 50))
                        _y = int(TARGET_Y + (h * 50))
                        _z = int(TARGET_Z)
        
                        voxel_editor.set_voxel_color(_x, _y, _z, find_similar_voxel_color(pixel[0], pixel[1], pixel[2]))
                        
        voxel_editor.finish()
            
    def on_mouse_right_click(self, game_context: GameContext):
        if not self.nes_env:
            self.nes_env = NESEnv(self.get_path("super-mario-bros-1.nes"))
            self.nes_keys = self.nes_env.get_keys_to_action()

            state = self.nes_env.reset()

            game_context.write_text(0xff00ff00, "Start NES Emulator..!\n")
            game_context.write_text(0xff00ff00, "Load `mario-bros-1.nes` ROM file.....")
        else:
            self.nes_env.close()
            self.nes_env = None
            game_context.write_text(0xffff0000, "Stop ROM..!\n")

    def on_stop(self):
        return None
