import umidiparser
import os
import time

from typing import List
from abc import ABC

from pyvoxelhorizon.enum import *
from pyvoxelhorizon.plugin import Plugin
from pyvoxelhorizon.plugin.type import *
from pyvoxelhorizon.plugin.util import *

PLUGIN_NAME = "MidiExamplePlugin"

class MidiExamplePlugin(Plugin, ABC):
    midi_events: List[umidiparser.MidiEvent] = []
    midi_event_index: int = 0
    midi_start_timestamp: float = 0
    midi_playback: int = 0

    def on_create(self):
        pass

    def on_destroy(self):
        pass

    def on_update(self):
        midi_new_playback = int((time.time() - self.midi_start_timestamp) * 1000)

        while self.midi_event_index < len(self.midi_events):
            midi_event = self.midi_events[self.midi_event_index]
            event_delta_ms = midi_event.delta_us / 1000

            if self.midi_playback + event_delta_ms > midi_new_playback:
                break

            self.midi_playback += event_delta_ms

            if midi_event.is_channel():
                if midi_event.status == umidiparser.NOTE_OFF or (midi_event.status == umidiparser.NOTE_ON and midi_event.velocity == 0):
                    self.game.print_line_to_system_dialog("Off {0}".format(midi_event.note))
                    self.game.game_controller.midi_write_note(midi_event.channel, False, midi_event.note, 0)
                elif midi_event.status == umidiparser.NOTE_ON:
                    self.game.print_line_to_system_dialog("On {0} {1}".format(midi_event.note, midi_event.velocity))
                    self.game.game_controller.midi_write_note(midi_event.channel, True, midi_event.note, midi_event.velocity)
                elif midi_event.status == umidiparser.PROGRAM_CHANGE:
                    self.game.print_line_to_system_dialog("Program {0} {1}".format(midi_event.status, midi_event.program))
                    self.game.game_controller.midi_change_program(midi_event.channel, midi_event.program)

            self.midi_event_index += 1

    def on_command(self, command: str) -> bool:
        if command == 'play':
            self.midi_events = []

            for midi_event in umidiparser.MidiFile(os.path.join(self.directory_path, "98_OVER.mid"), reuse_event_object=False):
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
