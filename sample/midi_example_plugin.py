import math
import os
import time
from abc import ABC
from ctypes import wintypes
from typing import List

import numpy
import umidiparser

from pyvoxelhorizon.plugin import Plugin
from pyvoxelhorizon.plugin.game.voxel import *
from pyvoxelhorizon.plugin.game.voxel.voxel_editor_online import cancel_all_editing_queue, wait_for_editing_queue
from pyvoxelhorizon.plugin.type import *
from pyvoxelhorizon.util.address_object import *

PLUGIN_NAME = "MidiExamplePlugin"
MIDI_NOTE_IMAGE_SCALE_RATIO = 0.05

MIDI_NOTE_IMAGE_NOTE_RANGE = 128
MIDI_NOTE_IMAGE_TIMING_RANGE = 128

MIDI_NOTE_IMAGE_DISPLAY_OFFSET_X = 0
MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Y = -1000
MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Z = 2350

MIDI_NOTE_IMAGE_BACKGROUND_COLOR = 11
MIDI_NOTE_IMAGE_CHANNEL_COLORS = [7, 18, 24, 27]

MIDI_NETWORK_MODE = False
MIDI_VISUALIZER_ONLINE_MODE = True
MIDI_VISUALIZER_MODE = True


def _separate_sysex_data(data: bytearray):
    data_list = []

    byte_array = bytearray([0xF0])

    for value in data:
        byte_array.append(value)

        if value == 0xF7:
            data_list.append(byte_array)
            byte_array = bytearray()

    return data_list


def _render_midi_notes(midi_file: umidiparser.MidiFile, rescale_ratio: float, buffer_for_y: int = 0):
    full_duration = 0

    for midi_event in midi_file:
        full_duration += midi_event.delta_us / 1000

    full_duration = math.ceil(full_duration)

    midi_channel_note_status_map = {}
    midi_notes = []
    playback = 0

    for midi_event in midi_file:
        playback += midi_event.delta_us

        if midi_event.is_channel():
            if midi_event.channel not in midi_channel_note_status_map:
                midi_channel_note_status_map[midi_event.channel] = {}

            if midi_event.status == umidiparser.NOTE_OFF or (midi_event.status == umidiparser.NOTE_ON and midi_event.velocity == 0):
                if midi_event.note in midi_channel_note_status_map[midi_event.channel]:
                    midi_channel_note_status_map[midi_event.channel][midi_event.note]["end_time"] = playback

                    midi_notes.append(midi_channel_note_status_map[midi_event.channel][midi_event.note])
                    del midi_channel_note_status_map[midi_event.channel][midi_event.note]
            elif midi_event.status == umidiparser.NOTE_ON:
                if midi_event.note not in midi_channel_note_status_map[midi_event.channel]:
                    midi_channel_note_status_map[midi_event.channel][midi_event.note] = {
                        "channel": midi_event.channel,
                        "note": midi_event.note,
                        "start_time": playback,
                        "end_time": None,
                        "velocity": midi_event.velocity,
                    }

    image = numpy.zeros([MIDI_NOTE_IMAGE_NOTE_RANGE, int(full_duration * rescale_ratio) + buffer_for_y, len(midi_channel_note_status_map.keys())], dtype=numpy.uint8)

    midi_channel_note_status_map_keys = list(midi_channel_note_status_map.keys())

    for midi_channel_index in range(len(midi_channel_note_status_map_keys)):
        midi_channel = midi_channel_note_status_map_keys[midi_channel_index]

        for midi_note in midi_notes:
            if midi_note['channel'] == midi_channel:
                midi_start_note_time = int((midi_note['start_time'] / 1000) * rescale_ratio)
                midi_end_note_time = int((midi_note['end_time'] / 1000) * rescale_ratio)

                image[midi_note['note'], midi_start_note_time:midi_end_note_time, midi_channel_index] = midi_note['velocity']

    return image


class MidiExamplePlugin(Plugin, ABC):
    midi_events: List[umidiparser.MidiEvent] = []
    midi_event_index: int = 0
    midi_start_timestamp: float = 0
    midi_playback: int = 0

    midi_note_image_previous: numpy.ndarray | None = None
    midi_note_image: numpy.ndarray = None

    def on_create(self):
        pass

    def on_destroy(self):
        pass

    def on_update(self):
        if not self.midi_event_index < len(self.midi_events):
            return

        voxel_editor = VoxelEditorOnline(self.game) if MIDI_VISUALIZER_ONLINE_MODE else VoxelEditorLocal(self.game)

        if self.midi_start_timestamp == -1:
            if MIDI_VISUALIZER_MODE:
                for note_index in range(MIDI_NOTE_IMAGE_NOTE_RANGE):
                    for timing_index in range(MIDI_NOTE_IMAGE_TIMING_RANGE):
                        voxel_editor.set_voxel_with_color(
                            MIDI_NOTE_IMAGE_DISPLAY_OFFSET_X + (note_index * 50),
                            MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Y + (timing_index * 50),
                            MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Z,
                            True,
                            get_voxel_color(MIDI_NOTE_IMAGE_BACKGROUND_COLOR)
                        )

            self.midi_start_timestamp = time.time()

        midi_new_playback = int((time.time() - self.midi_start_timestamp) * 1000)

        if MIDI_VISUALIZER_MODE:
            midi_note_image_crop_start = int(midi_new_playback * MIDI_NOTE_IMAGE_SCALE_RATIO)
            midi_note_image_crop_end = midi_note_image_crop_start + MIDI_NOTE_IMAGE_TIMING_RANGE
            midi_note_image_crop = self.midi_note_image[:, midi_note_image_crop_start:midi_note_image_crop_end, :]

            if self.midi_note_image_previous is not None:
                changed_indices = numpy.where(midi_note_image_crop != self.midi_note_image_previous)
                changed_count = len(changed_indices[0])
                changed_dim1_indices = list(changed_indices[0])
                changed_dim2_indices = list(changed_indices[1])
                changed_dim3_indices = list(changed_indices[2])

                for changed_index in range(changed_count):
                    note_index = changed_dim1_indices[changed_index]
                    timing_index = changed_dim2_indices[changed_index]
                    channel_index = changed_dim3_indices[changed_index]

                    value = midi_note_image_crop[note_index, timing_index, channel_index]

                    if value == 0:
                        voxel_editor.set_voxel(
                            MIDI_NOTE_IMAGE_DISPLAY_OFFSET_X + (note_index * 50),
                            MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Y + (timing_index * 50),
                            MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Z - (((channel_index % 7) + 1) * 50),
                            False
                        )
                    else:
                        color = VOXEL_COLOR_PALETTE[MIDI_NOTE_IMAGE_CHANNEL_COLORS[channel_index % len(MIDI_NOTE_IMAGE_CHANNEL_COLORS)]]

                        voxel_editor.set_voxel_with_color(
                            MIDI_NOTE_IMAGE_DISPLAY_OFFSET_X + (note_index * 50),
                            MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Y + (timing_index * 50),
                            MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Z - (((channel_index % 7) + 1) * 50),
                            True,
                            color
                        )

            self.midi_note_image_previous = midi_note_image_crop

        voxel_editor.finish()

        # Re-define playback time for fix not synced midi player
        midi_new_playback = int((time.time() - self.midi_start_timestamp) * 1000)

        if not MIDI_NETWORK_MODE:
            while self.midi_event_index < len(self.midi_events):
                midi_event = self.midi_events[self.midi_event_index]
                event_delta_ms = midi_event.delta_us / 1000

                if self.midi_playback + event_delta_ms > midi_new_playback:
                    break

                self.midi_playback += event_delta_ms

                if midi_event.status == umidiparser.SYSEX:
                    sysex_datas = _separate_sysex_data(midi_event.data)

                    for sysex_data in sysex_datas:
                        sysex_bytes = (wintypes.BYTE * len(sysex_data))(*sysex_data)
                        self.game.controller.midi_sysex_message_immediately(cast_address(get_address(sysex_bytes), wintypes.BYTE), len(sysex_data))

                if midi_event.is_channel():
                    if midi_event.status == umidiparser.NOTE_OFF or (midi_event.status == umidiparser.NOTE_ON and midi_event.velocity == 0):
                        self.game.controller.midi_note_off_immediately(midi_event.channel, midi_event.note, 0)
                    elif midi_event.status == umidiparser.NOTE_ON:
                        self.game.controller.midi_note_on_immediately(midi_event.channel, midi_event.note, midi_event.velocity)
                    elif midi_event.status == umidiparser.PROGRAM_CHANGE:
                        self.game.controller.midi_change_program_immediately(midi_event.channel, midi_event.program)
                    elif midi_event.status == umidiparser.CONTROL_CHANGE:
                        self.game.controller.midi_change_control_immediately(midi_event.channel, midi_event.control, midi_event.value)
                    elif midi_event.status == umidiparser.PITCHWHEEL:
                        self.game.controller.midi_change_pitch_bend_immediately(midi_event.channel, midi_event.data[0], midi_event.data[1])

                self.midi_event_index += 1
        else:
            while self.midi_event_index < len(self.midi_events):
                midi_event = self.midi_events[self.midi_event_index]
                event_delta_ms = midi_event.delta_us / 1000

                if self.midi_playback + event_delta_ms > midi_new_playback:
                    break

                self.midi_playback += event_delta_ms
                self.midi_event_index += 1

    def on_command(self, command: str) -> bool:
        tokens = command.split(" ")

        if tokens[0].lower() == "midi_play":
            midi_file = umidiparser.MidiFile(os.path.join(self.directory_path, tokens[1]), reuse_event_object=False)

            if MIDI_VISUALIZER_MODE:
                self.midi_note_image = _render_midi_notes(midi_file, MIDI_NOTE_IMAGE_SCALE_RATIO, buffer_for_y=MIDI_NOTE_IMAGE_TIMING_RANGE)
            self.midi_events = []

            for midi_event in midi_file:
                self.midi_events.append(midi_event)

            self.midi_note_image_previous = None
            self.midi_event_index = 0
            self.midi_start_timestamp = -1
            self.midi_playback = 0

            if MIDI_NETWORK_MODE:
                self.game.controller.enable_broadcast_mode_immediately()

                self.game.controller.midi_begin_push_message()

                local_midi_playback = 0
                local_midi_event_index = 0

                while local_midi_event_index < len(self.midi_events):
                    midi_event = self.midi_events[local_midi_event_index]
                    event_delta_ms = midi_event.delta_us / 1000

                    local_midi_playback += event_delta_ms

                    if midi_event.status == umidiparser.SYSEX:
                        sysex_datas = _separate_sysex_data(midi_event.data)

                        for sysex_data in sysex_datas:
                            sysex_bytes = (wintypes.BYTE * len(sysex_data))(*sysex_data)
                            self.game.controller.midi_push_sysex_message(cast_address(get_address(sysex_bytes), wintypes.BYTE), len(sysex_data), int(local_midi_playback))

                    if midi_event.is_channel():
                        if midi_event.status == umidiparser.NOTE_OFF or (midi_event.status == umidiparser.NOTE_ON and midi_event.velocity == 0):
                            self.game.controller.midi_push_note_off(midi_event.channel, midi_event.note, 0, int(local_midi_playback))
                        elif midi_event.status == umidiparser.NOTE_ON:
                            self.game.controller.midi_push_note_on(midi_event.channel, midi_event.note, midi_event.velocity, int(local_midi_playback))
                        elif midi_event.status == umidiparser.PROGRAM_CHANGE:
                            self.game.controller.midi_push_change_program(midi_event.channel, midi_event.program, int(local_midi_playback))
                        elif midi_event.status == umidiparser.CONTROL_CHANGE:
                            self.game.controller.midi_push_change_control(midi_event.channel, midi_event.control, midi_event.value, int(local_midi_playback))
                        elif midi_event.status == umidiparser.PITCHWHEEL:
                            self.game.controller.midi_push_change_pitch_bend(midi_event.channel, midi_event.data[0], midi_event.data[1], int(local_midi_playback))

                    local_midi_event_index += 1

                self.game.controller.midi_end_push_message()

            return True

        if tokens[0].lower() == "midi_stop":
            off_checks = {}

            for midi_event in self.midi_events:
                if midi_event.is_channel() and midi_event.status == umidiparser.NOTE_ON:
                    if midi_event.channel not in off_checks:
                        off_checks[midi_event.channel] = {}

                    if midi_event.note not in off_checks[midi_event.channel]:
                        off_checks[midi_event.channel][midi_event.note] = True

                        self.game.controller.midi_note_off_immediately(midi_event.channel, midi_event.note, 0)

            self.midi_events = []
            self.midi_event_index = 0
            self.midi_start_timestamp = -1
            self.midi_playback = 0

            if MIDI_NETWORK_MODE:
                self.game.controller.disable_broadcast_mode_immediately()
                self.game.controller.midi_reset()

            if MIDI_VISUALIZER_MODE:
                if MIDI_VISUALIZER_ONLINE_MODE:
                    cancel_all_editing_queue(self.game)

                voxel_editor = VoxelEditorOnline(self.game) if MIDI_VISUALIZER_ONLINE_MODE else VoxelEditorLocal(self.game)

                for note_index in range(MIDI_NOTE_IMAGE_NOTE_RANGE):
                    for timing_index in range(MIDI_NOTE_IMAGE_TIMING_RANGE):
                        for depth_index in range(0, 8):
                            if voxel_editor.get_voxel(
                                    MIDI_NOTE_IMAGE_DISPLAY_OFFSET_X + (note_index * 50),
                                    MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Y + (timing_index * 50),
                                    MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Z - (depth_index * 50)
                            ):
                                voxel_editor.set_voxel_with_color(
                                    MIDI_NOTE_IMAGE_DISPLAY_OFFSET_X + (note_index * 50),
                                    MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Y + (timing_index * 50),
                                    MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Z - (depth_index * 50),
                                    False
                                )

                voxel_editor.finish()

                if MIDI_VISUALIZER_ONLINE_MODE:
                    wait_for_editing_queue()

            return True

        return False

    def on_mouse_click(self, x: int, y: int, button_type: MouseButtonType, pressed: bool) -> bool:
        return False

    def on_mouse_move(self, x: int, y: int) -> bool:
        return False

    def on_mouse_wheel(self, x: int, y: int, wheel: int) -> bool:
        return False

    def on_key(self, key_type: KeyType, pressed: bool) -> bool:
        return False

    def on_pad(self, button_type: PadButtonType, pressed: bool) -> bool:
        return False
