# -*- coding: utf-8 -*-

import config as cfg
import shutil

from textgenrnn import textgenrnn


def train_network(name):
    cfg.generate_training_config(name)
    config = cfg.load_config()

    textgen = textgenrnn()
    textgen.train_from_file(config.get('FilePaths', 'source_messages'), 
                            new_model=True,
                            num_epochs=600,
                            gen_epochs=120,
                            dropout=0.1,
                            train_size=0.9,
                            word_level=True,
                            batch_size=256)

    shutil.move('textgenrnn_weights.hdf5', config.get('Model', 'weights'))
    shutil.move('textgenrnn_vocab.json', config.get('Model', 'vocab'))
    shutil.move('textgenrnn_config.json', config.get('Model', 'config'))


if __name__ == '__main__':
	train_network('')
