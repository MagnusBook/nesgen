from base.base_model import BaseModel
import tensorflow as tf


class Biaxial(BaseModel):
    def __init__(self, config):
        super(Biaxial, self).__init__(config)
        self.build_model()
        self.init_saver()

    def build_model(self):
        self.is_training = tf.placeholder(tf.bool)

        self.x = tf.placeholder(tf.float32, shape=[None] + self.config.state_size)
        self.y = tf.placeholder(tf.float32, shape=[None, 10])

        # network architecture
        def lstm_cell(size, activation=None):
            return tf.keras.layers.LSTMCell(size, activation=activation, dropout=self.config.dropout) if activation else tf.keras.layers.LSTMCell(size, dropout=self.config.dropout)
        self.time_model = tf.keras.layers.StackedRNNCells([lstm_cell(s) for s in self.config.t_layer_sizes])

        # p_input_size = self.config.t_layer_sizes[-1] + 2
        self.pitch_model = tf.keras.layers.StackedRNNCells([lstm_cell(s, tf.nn.sigmoid if i == len(self.config.p_layer_sizes) - 1 else None) for i, s in enumerate(self.config.p_layer_sizes)])

    def init_saver(self):
        self.saver = tf.train.Saver(max_to_keep=self.config.max_to_keep)
