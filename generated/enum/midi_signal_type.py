import ctypes
import ctypes.wintypes as wintypes

from pyvoxelhorizon.util import *

MIDI_SIGNAL_TYPE_NOTE = 0
MIDI_SIGNAL_TYPE_CONTROL = 1


def get_midi_signal_type_string(value: int):
    if value == 0:
        return 'MIDI_SIGNAL_TYPE_NOTE'
    if value == 1:
        return 'MIDI_SIGNAL_TYPE_CONTROL'
    
    return 'MIDI_SIGNAL_TYPE_UNKNOWN'
