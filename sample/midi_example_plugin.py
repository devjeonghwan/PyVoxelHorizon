import math

import umidiparser
import os
import time
import numpy

from typing import List
from abc import ABC

from pyvoxelhorizon.enum import *
from pyvoxelhorizon.plugin import Plugin
from pyvoxelhorizon.plugin.game import VoxelEditor, get_voxel_color, VOXEL_COLOR_PALETTE
from pyvoxelhorizon.plugin.type import *
from pyvoxelhorizon.plugin.util import *


PLUGIN_NAME = "MidiExamplePlugin"
MIDI_NOTE_IMAGE_SCALE_RATIO = 0.05

MIDI_NOTE_IMAGE_NOTE_RANGE = 128
MIDI_NOTE_IMAGE_TIMING_RANGE = 128

MIDI_NOTE_IMAGE_DISPLAY_OFFSET_X = 0
MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Y = -1000
MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Z = 2000

MIDI_NOTE_IMAGE_BACKGROUND_COLOR = 11
MIDI_NOTE_IMAGE_CHANNEL_COLORS = [7, 18, 24, 27]


def render_midi_notes(midi_file: umidiparser.MidiFile, rescale_ratio: float, buffer_for_y: int = 0):
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

    midi_note_image_previous: numpy.ndarray = None
    midi_note_image: numpy.ndarray = None

    def on_create(self):
        pass

    def on_destroy(self):
        pass

    def on_update(self):
        if not self.midi_event_index < len(self.midi_events):
            return

        voxel_editor = VoxelEditor(self.game)

        if self.midi_event_index == 0:
            for note_index in range(MIDI_NOTE_IMAGE_NOTE_RANGE):
                for timing_index in range(MIDI_NOTE_IMAGE_TIMING_RANGE):
                    voxel_editor.add_voxel(
                        MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Y + (note_index * 50),
                        MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Y + (timing_index * 50),
                        MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Z,
                        get_voxel_color(MIDI_NOTE_IMAGE_BACKGROUND_COLOR)
                    )

            # Reset start timestamp for lagging
            self.midi_start_timestamp = time.time()

        midi_new_playback = int((time.time() - self.midi_start_timestamp) * 1000)

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
                    color = VOXEL_COLOR_PALETTE[MIDI_NOTE_IMAGE_BACKGROUND_COLOR]
                else:
                    color = VOXEL_COLOR_PALETTE[MIDI_NOTE_IMAGE_CHANNEL_COLORS[channel_index % len(MIDI_NOTE_IMAGE_CHANNEL_COLORS)]]

                voxel_editor.set_voxel_color(
                    MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Y + (note_index * 50),
                    MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Y + (timing_index * 50),
                    MIDI_NOTE_IMAGE_DISPLAY_OFFSET_Z,
                    color
                )

        self.midi_note_image_previous = midi_note_image_crop

        voxel_editor.finish()

        while self.midi_event_index < len(self.midi_events):
            midi_event = self.midi_events[self.midi_event_index]
            event_delta_ms = midi_event.delta_us / 1000

            if self.midi_playback + event_delta_ms > midi_new_playback:
                break

            self.midi_playback += event_delta_ms

            if midi_event.is_channel():
                if midi_event.status == umidiparser.NOTE_OFF or (midi_event.status == umidiparser.NOTE_ON and midi_event.velocity == 0):
                    self.game.game_controller.midi_write_note(midi_event.channel, False, midi_event.note, 0)
                elif midi_event.status == umidiparser.NOTE_ON:
                    self.game.game_controller.midi_write_note(midi_event.channel, True, midi_event.note, midi_event.velocity)
                elif midi_event.status == umidiparser.PROGRAM_CHANGE:
                    self.game.game_controller.midi_change_program(midi_event.channel, midi_event.program)

            self.midi_event_index += 1

    def on_command(self, command: str) -> bool:
        if command == 'play':
            midi_file = umidiparser.MidiFile(os.path.join(self.directory_path, "98_OVER.mid"), reuse_event_object=False)
            self.midi_note_image = render_midi_notes(midi_file, MIDI_NOTE_IMAGE_SCALE_RATIO, buffer_for_y=MIDI_NOTE_IMAGE_TIMING_RANGE)
            self.midi_events = []

            for midi_event in midi_file:
                self.midi_events.append(midi_event)

            self.midi_event_index = 0
            self.midi_start_timestamp = time.time()
            self.midi_playback = 0

            return True

        if command == 'stop':
            off_checks = {}

            for midi_event in self.midi_events:
                if midi_event.is_channel() and midi_event.status == umidiparser.NOTE_ON:
                    if midi_event.channel not in off_checks:
                        off_checks[midi_event.channel] = {}

                    if midi_event.note not in off_checks[midi_event.channel]:
                        off_checks[midi_event.channel][midi_event.note] = True

                        self.game.game_controller.midi_write_note(midi_event.channel, False, midi_event.note, 0)

            self.midi_events = []
            self.midi_event_index = 0
            self.midi_start_timestamp = time.time()
            self.midi_playback = 0

            return True

        return False

    def on_mouse_click(self, x: int, y: int, button_type: MouseButtonType, pressed: bool) -> bool:
        return False

    def on_mouse_move(self, x: int, y: int) -> bool:
        return False

    def on_mouse_wheel(self, wheel: int) -> bool:
        return False

    def on_key(self, key_type: KeyType, pressed: bool) -> bool:
        return False

    def on_pad(self, button_type: PadButtonType, pressed: bool) -> bool:
        return False
