import os
import music21 as m21
from utils.statematrix  import StateMatrixBuilderSimple

count = 0
bad_count = 0
d = "data/valid"

for (dirpath, dirnames, filenames) in os.walk(d):
    for fname in filenames:
        fpath = "{}/{}".format(d, fname)
        mf = m21.midi.MidiFile()
        mf.open(fpath)
        mf.read()
        mf.close()
        midi_data = m21.midi.translate.midiFileToStream(mf)
        print(fname)
        sm = StateMatrixBuilderSimple(0, 127, 16)
        s = sm.stream_to_statematrix(midi_data)
        n = sm.statematrix_to_stream(s)
        f = n.flat
        for note in f.notes:
            print(note)
