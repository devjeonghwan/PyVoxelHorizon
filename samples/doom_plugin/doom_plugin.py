from voxel_horizon_plugin import VoxelHorizonPlugin
from pyvoxelhorizon.game.object import *
from pyvoxelhorizon.game.helper import VoxelEditor

import vizdoom as vzd

import random
import math
import time
import numpy
import cv2
import os

PLUGIN_NAME     = "DOOMPlugin"

TARGET_X        = 0
TARGET_Y        = 0
TARGET_Z        = 0

WIDTH = 120
HEIGHT = 100
FRAME_RATE = 10.0
FRAME_RATE_INTERVAL = 1 / FRAME_RATE

class DOOMPlugin(VoxelHorizonPlugin):
    def on_initialize(self, game_context: GameContext):
        self.initialized = False

        self.game = None
        
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
        
        if self.game:
            now = time.time()
            interval = now - self.last_time

            if interval > FRAME_RATE_INTERVAL:
                self.last_time = now

# Available buttons: ['ATTACK', 'USE', 'TURN_LEFT', 'TURN_RIGHT', 'MOVE_RIGHT', 'MOVE_LEFT', 'MOVE_FORWARD', 'MOVE_BACKWARD', 'TURN_LEFT_RIGHT_DELTA', 'LOOK_UP_DOWN_DELTA']
                actions = [False, False, False, False, False, False, False, False, False, False]

                if game_context.is_key_press(0x41): # A
                    actions[5] = True
                if game_context.is_key_press(0x57): # W
                    actions[6] = True
                if game_context.is_key_press(0x53): # S
                    actions[7] = True
                if game_context.is_key_press(0x44): # D
                    actions[4] = True
                    
                if game_context.is_key_press(0x4F):
                    actions[0] = True
                if game_context.is_key_press(0x4C):
                    actions[1] = True
                
                if game_context.is_key_press(0x25):
                    actions[2] = True
                if game_context.is_key_press(0x27):
                    actions[3] = True
                
                state = self.game.get_state()
                self.game.make_action(actions)

                resized = cv2.resize(state.screen_buffer, dsize=(WIDTH, HEIGHT), interpolation=cv2.INTER_NEAREST)
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
        if not self.game:
            self.game = vzd.DoomGame()

            self.game.load_config(os.path.join(vzd.scenarios_path, "cig.cfg"))
            self.game.set_doom_scenario_path(os.path.join(vzd.scenarios_path, "doom2.wad"))
            self.game.set_doom_map("map01")
            self.game.set_screen_resolution(vzd.ScreenResolution.RES_160X120)

            self.game.set_screen_format(vzd.ScreenFormat.RGB24)
            self.game.set_automap_buffer_enabled(True)
            self.game.set_objects_info_enabled(True)
            self.game.set_sectors_info_enabled(True)

            self.game.set_render_hud(True)
            self.game.set_render_crosshair(True)
            self.game.set_render_weapon(True)
            self.game.set_render_decals(True)
            self.game.set_render_particles(True)
            self.game.set_render_effects_sprites(True)
            self.game.set_render_messages(True)
            self.game.set_render_corpses(True)
            self.game.set_render_screen_flashes(True)  

            self.game.set_available_game_variables([vzd.GameVariable.AMMO2])
            print("Available buttons:", [b.name for b in self.game.get_available_buttons()])

            self.game.set_available_game_variables([vzd.GameVariable.AMMO2])
            print("Available game variables:", [v.name for v in self.game.get_available_game_variables()], )

            self.game.set_window_visible(False)
            self.game.set_mode(vzd.Mode.PLAYER)

            self.game.init()
            self.game.new_episode()

            game_context.write_text(0xff00ff00, "Start VIZ Doom..!\n")
        else:
            self.game.close()
            self.game = None
            game_context.write_text(0xffff0000, "Stop VIZ Doom..!\n")

    def on_stop(self):
        return None
