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
            fpath = "{}/{}".format(d, fname)
            mf = midi.MidiFile()
            mf.open(fpath)
            mf.read()
            mf.close()
            midi_data = midi.translate.midiFileToStream(mf)
            print('test')
            print(midi_data.elements)
            print(midi_data[0].elements)
            print(fname)
            midi_data = pretty_midi.PrettyMIDI(fpath)
            if midi_data.get_end_time() < 9:
                os.remove(fpath)
        except:
            print('BAD')

print('Count: ', count)
print("Bad Count: ", bad_count)
