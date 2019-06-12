from base.base_model import BaseModel
import tensorflow as tf


class Biaxial(BaseModel):
    def __init__(self, config, name):
        super(Biaxial, self).__init__(config)
        index = config.biaxial_names.index(name)
        self.name = self.config.biaxial_names[index]
        self.t_layer_sizes = self.config.t_layer_sizes[index]
        self.p_layer_sizes = self.config.p_layer_sizes[index]
        self.build_model()
        self.init_saver()

    def build_model(self):
        self.is_training = tf.placeholder(tf.bool)

        def lstm_cell(size, activation=None):
            return tf.keras.layers.LSTMCell(size, activation=activation, dropout=self.config.dropout) if activation else tf.keras.layers.LSTMCell(size, dropout=self.config.dropout)
        self.time_model = tf.keras.layers.StackedRNNCells([lstm_cell(s) for s in self.t_layer_sizes])

        # p_input_size = self.config.t_layer_sizes[-1] + 2
        self.pitch_model = tf.keras.layers.StackedRNNCells([lstm_cell(s, tf.nn.sigmoid if i == len(self.p_layer_sizes) - 1 else None) for i, s in enumerate(self.p_layer_sizes)])

    def loss(self, labels, predictions):
        return tf.losses.log_loss(labels, predictions)

    def setup_predict(self):
        self.predict_seed = tf.Tensor()

    def init_saver(self):
        self.saver = tf.train.Saver(max_to_keep=self.config.max_to_keep)
