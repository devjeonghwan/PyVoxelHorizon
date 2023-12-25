import umidiparser

midi_file = umidiparser.MidiFile("YS3TITLE.mid", reuse_event_object=False)

index_track = 0

for midi_event in midi_file:
    if midi_event.status == umidiparser.SYSEX:
        print(midi_event)
        print(list(midi_event.data))

# for midi_track in midi_file.tracks:
#
#     for midi_event in midi_track:
#         if midi_event.status == umidiparser.SYSEX:
#             print(list(midi_event.data))
        # if midi_event.status != umidiparser.NOTE_ON and midi_event.status != umidiparser.INSTRUMENT_NAME and midi_event.status != umidiparser.MARKER:
        #     print(midi_event)

    index_track += 1