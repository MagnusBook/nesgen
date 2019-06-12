import random
import numpy as np
import os
import pickle
import music21 as m21
from tqdm import tqdm
from utils.statematrix import StateMatrixBuilderSimple
from utils.features import FeatureBuilderSimple
import pretty_midi


class DataLoader:
    def __init__(self, config, preprocess):
        self.config = config
        self.feature_builder = FeatureBuilderSimple(
            config.lower_bound, config.upper_bound)
        self.sm_builder = StateMatrixBuilderSimple(
            config.lower_bound, config.upper_bound, config.quantization)
        # load data here
        if preprocess:
            self.pieces = self.generate_statematrices()
        else:
            self.pieces = self.load_statematrices()

    def generate_statematrices(self):
        pieces = {}
        paths = self.get_file_paths(self.config.train_dir)

        print('Performing preprocessing')
        pbar = tqdm(paths)
        if not os.path.exists(self.config.sm_dir):
            os.makedirs(self.config.sm_dir)
        for p in pbar:
            pbar.set_description("Processing {}".format(p))
            sm = []
            piece = m21.converter.parse(p, format="MIDI")
            midi_data = pretty_midi.PrettyMIDI(p)

            # this part deals with missing channels in the data by converting an empty part
            # to a statematrix when a channel does not exist
            instruments = [instrument.name.upper() for instrument in midi_data.instruments]
            part_counter = 0
            for instrument in self.config.biaxial_names:
                if instrument in instruments:
                    sm.append(self.sm_builder.part_to_statematrix(piece.parts[part_counter]))
                    part_counter += 1
                else:
                    sm.append(self.sm_builder.part_to_statematrix(m21.stream.Part()))

            pickle.dump(sm, open(os.path.join(self.config.sm_dir,
                                                os.path.basename(p).split(".")[0] + ".pkl"), "wb"))
            name = os.path.basename(p)
            pieces[name] = sm

        return pieces

    def load_statematrices(self):
        pieces = {}
        paths = self.get_file_paths(self.config.sm_dir)

        for p in paths:
            name = os.path.basename(p)
            with open(p, "rb") as f:
                pieces[name] = pickle.load(f)

        return pieces

    def get_file_paths(self, directory):
        return [os.path.join(directory, f) for f in os.listdir(directory)]

    def sample_sequence(self):
        # The loop 'assures' the method to return a sequence.
        for i in range(100):
            try:
                piece_output = random.choice(list(self.pieces.values()))
                start = random.randrange(
                    0, len(piece_output[0]) - self.config.seq_len, self.config.division_len)
                break
            except:
                pass

        if i == 99:
            raise ValueError("No valid segment found")

        return np.array(piece_output), start

    def get_piece_segment(self, piece_sample, start):
        seg_out = piece_sample[start:start+self.config.seq_len]
        seg_in = self.feature_builder.note_state_matrix_to_input_form(seg_out)

        return seg_in, seg_out

    def next_batch(self):
        input = []
        output = []
        batch = [self.sample_sequence() for _ in range(self.config.batch_size)]
        test = range(len(self.config.biaxial_names))
        for j in range(len(self.config.biaxial_names)):
            i, o = zip(*[self.get_piece_segment(b[0][j], int(b[1])) for b in batch])
            input.append(np.array(i))
            output.append(np.array(o))

        return input, output
