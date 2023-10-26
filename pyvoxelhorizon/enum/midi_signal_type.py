MIDI_SIGNAL_TYPE_NOTE = 0
MIDI_SIGNAL_TYPE_CONTROL = 1
MIDI_SIGNAL_TYPE_PROGRAM = 2
MIDI_SIGNAL_TYPE_COUNT = 3


def get_midi_signal_type_string(value: int):
    if value == 0:
        return 'MIDI_SIGNAL_TYPE_NOTE'
    if value == 1:
        return 'MIDI_SIGNAL_TYPE_CONTROL'
    if value == 2:
        return 'MIDI_SIGNAL_TYPE_PROGRAM'
    if value == 3:
        return 'MIDI_SIGNAL_TYPE_COUNT'
    
    return 'MIDI_SIGNAL_TYPE_UNKNOWN'
