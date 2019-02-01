from os import walk
import pretty_midi


for (dirpath, dirnames, filenames) in walk("data/train"):
  for fname in  filenames:
    midi_data = pretty_midi.PrettyMIDI('data/train/')
    for semi_tone in range(1,12):
      for instrument in midi_data.instruments:
        if not instrument.name == 'no':
          for note in instrument.notes:
            note.pitch += semi_tone
      audio_data = midi_data.synthesize()
      
