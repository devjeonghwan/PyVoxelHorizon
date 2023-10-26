import ctypes
import ctypes.wintypes as wintypes


class MIDI_DEVICE_INFO(ctypes.Structure):
    _fields_ = (
        ('wch_name', wintypes.WCHAR * 128),
        ('wch_id', wintypes.WCHAR * 128),
    )

    def __repr__(self):
        return f'MIDI_DEVICE_INFO(wch_name={self.wch_name}, wch_id={self.wch_id})'
