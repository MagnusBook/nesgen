import tensorflow as tf


class BaseModel:
    def __init__(self, config):
        self.config = config
        self.saver = None
        self.init_global_step()
        self.init_current_epoch()

    def save(self, sess):
        print("Saving model...")
        self.saver.save(sess, self.config.checkpoint_dir,
                        self.global_step_tensor)
        print("Model saved")

    def load(self, sess):
        latest_checkpoint = tf.train.latest_checkpoint(
            self.config.checkpoint_dir)
        if latest_checkpoint:
            print("Loading model checkpoint {} ...\n".format(latest_checkpoint))
            self.saver.restore(sess, latest_checkpoint)
            print("Model loaded")

    def init_current_epoch(self):
        with tf.variable_scope("current_epoch"):
            self.current_epoch_tensor = tf.Variable(
                0, trainable=False, name="current_epoch")
            self.increment_current_epoch_tensor = tf.assign(
                self.current_epoch_tensor, self.current_epoch_tensor + 1)

    def init_global_step(self):
        with tf.variable_scope("global_step"):
            self.global_step_tensor = tf.Variable(
                0, trainable=False, name="global_step")

    def init_saver(self):
        # just copy the following line in your child class
        # self.saver = tf.train.Saver(max_to_keep=self.config.max_to_keep)
        raise NotImplementedError

    def build_model(self):
        raise NotImplementedError
