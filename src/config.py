# -*- coding: utf-8 -*-

import configparser
import sys


DATA_DIR = 'src/data/'


def generate_config():
    config = configparser.ConfigParser()

    config['FilePaths'] = { 
        'source_data': DATA_DIR + 'src.json',
        'source_messages': DATA_DIR + 'srcmsg.txt',
        'generated_messages': DATA_DIR + 'genmsg.txt',
        'messages': DATA_DIR + 'msg.txt'
    }

    config['Extract'] = { 
        'user': 39
    }

    config['Model'] = {
        'weights': DATA_DIR + 'textgenrnn_weights.hdf5',
        'vocab': DATA_DIR + 'textgenrnn_vocab.json',
        'config': DATA_DIR + 'textgenrnn_config.json',
        'generated_lines': 1000000
    }

    config['ID'] = {
        'channel': '',
        'emotes': '<:pepega:545748645270519829>,<:pepga:545748657904025620>',
    }

    config['Settings'] = {
        'token': '',
        'sleep_time': 30,
        'emote_chance': 10,
        'combo_chance': 75,
        'typing_time': 1.5
    }

    with open(DATA_DIR + 'config.ini', 'w') as configfile:
        config.write(configfile)


def load_config():
    config = configparser.ConfigParser()
    config_file = DATA_DIR + 'config.ini'
    config.read(config_file)
    return config
