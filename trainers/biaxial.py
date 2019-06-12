import numpy as np
from base.base_train import BaseTrain
from tqdm import trange


class Trainer(BaseTrain):
    def __init__(self, sess, model, data, config, logger):
        super(Trainer, self).__init__(sess, model, data, config, logger)
        scores = data.get_file_paths(self.config.sm_dir)
        split = int(len(scores) * (1- self.config.validation_split))
        self.train_scores = scores[:split]
        self.val_pieces = scores[split:]

    def train(self):
        for _ in trange(self.config.num_epochs):
            self.train_epoch()

    def train_epoch(self):
        losses = []
        accs = []
        for _ in trange(len(scores)):
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
