import tensorflow as tf
from base.base_model import BaseModel
from models.biaxial import Biaxial


class Model(BaseModel):
    def __init__(self, config):
        super(Model, self).__init__(config)
        self.build_model()
        self.init_saver()

    def build_model(self):
        self.is_training = tf.placeholder(tf.bool)

        self.p1_model = Biaxial(self.config, self.config.biaxial_names[0])
        self.p2_model = Biaxial(self.config, self.config.biaxial_names[1])
        self.tr_model = Biaxial(self.config, self.config.biaxial_names[2])
        self.no_model = Biaxial(self.config, self.config.biaxial_names[3])

        # TODO: Add composer component

    def loss(self, labels, predictions):
        return tf.losses.log_loss(labels, predictions)

    def init_saver(self):
        self.saver = tf.train.Saver(max_to_keep=self.config.max_to_keep)
