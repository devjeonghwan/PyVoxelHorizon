import ctypes
import ctypes.wintypes as wintypes

class MidiNote(ctypes.Structure):
    _fields_ = (
        ('dw_relative_tick', wintypes.DWORD),
        ('dw_value', wintypes.DWORD),
    )

    def __repr__(self):
        return f'MidiNote(dw_relative_tick={self.dw_relative_tick}, dw_value={self.dw_value})'
