from base.base_train import BaseTrain
from tqdm import tqdm
import numpy as np
import tensorflow as tf


class Trainer(BaseTrain):
    def __init__(self, sess, model, data, config, logger):
        super(Trainer, self).__init__(sess, model, data, config, logger)

    def validate(self, repeat=3):
        sub_val = []
        for i in range(repeat):
            sample, start = self.data.sample_sequence()
            xIpt, xOpt = map(np.array, self.data.get_piece_segment(sample, start))
            seed_length = int(len(xIpt) / 2)
            val = self.sess.run(self.model.loss(xOpt[seed_length:seed_length+16], ))

    def train_epoch(self):
        loop = tqdm(range(self.config.num_epochs))
        losses = []
        accs = []
        for _ in loop:
            loss, acc = self.train_step()
            losses.append(loss)
            accs.append(acc)
        loss = np.mean(losses)
        acc = np.mean(accs)

        current_it = self.model.global_step_tensor.eval(self.sess)
        summaries_dict = {
            'loss': loss,
            'acc': acc
        }
        self.logger.summarize(current_it, summaries_dict=summaries_dict)
        self.model.save(self.sess)

    def train_step(self):
        batch_x, batch_y = next(self.data.next_batch(self.config.batch_size))
        feed_dict = {self.model.x: batch_x, self.model.y: batch_y, self.model.is_training: True}
        _, loss, acc = self.sess.run([self.model.train_step, self.model.cross_entropy, self.model.accuracy], feed_dict=feed_dict)
        return loss, acc
