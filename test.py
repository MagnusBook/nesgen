import os
from music21 import midi
import music21 as m21
import pretty_midi

count = 0
bad_count = 0
d = "data/valid"

for (dirpath, dirnames, filenames) in os.walk(d):
    for fname in filenames:
        try:
            # mf = midi.MidiFile()
            # mf.open('data/test/' + fname)
            # mf.read()
            # mf.close()
            # #print(midi.translate.midiEventsToTimeSignature(mf.tracks[0][0]))
            # midi_data = midi.translate.midiFileToStream(mf).flat
            print(fname)
            fpath = "{}/{}".format(d, fname)
            midi_data = pretty_midi.PrettyMIDI(fpath)
            if midi_data.get_end_time() < 9:
                os.remove(fpath)
        except:
            print('BAD')

print('Count: ', count)
print("Bad Count: ", bad_count)
