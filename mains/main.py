import tensorflow as tf

# from data_loader.data_loader import DataLoader
from models.biaxial import Biaxial
from trainers.trainer import Trainer
from utils.config import process_config
from utils.dirs import create_dirs
from utils.logger import Logger
from utils.utils import get_args


def main():
    try:
        args = get_args()
        config = process_config(args.config)

    except:
        print("Missing or invalid arguments")
        exit(0)

    create_dirs([config.summary_dir, config.checkpoint_dir])
    sess = tf.Session()
    # data = DataLoader(config)
    model = Biaxial(config)
    logger = Logger(sess, config)
    trainer = Trainer(sess, model, data, config, logger)
    model.load(sess)
    trainer.train()


if __name__ == '__main__':
    main()
