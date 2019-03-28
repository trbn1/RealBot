# -*- coding: utf-8 -*-

import configparser
import sys


DATA_DIR = 'src/data/'


def generate_training_config():
    config = configparser.ConfigParser()

    config['FilePaths'] = {
        'source_data': DATA_DIR + 'src.json',
        'source_messages': DATA_DIR + 'srcmsg.txt',
        'generated_messages': DATA_DIR + 'genmsg.txt',
        'messages': DATA_DIR + 'msg.txt',
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

    try:
        with open(DATA_DIR + 'config.ini', 'w') as configfile:
            config.write(configfile)
    except:
        print('Error: Failed to write configuration file.')
        sys.exit(1)


def generate_bot_config():
    config = configparser.ConfigParser()

    bot_1 = ''
    config[bot_1] = {
        'name': bot_1,
        'messages': DATA_DIR + bot_1 + '_msg.txt',
        'channel': '',
        'emotes': '',
        'token': '',
        'sleep_time': 30,
        'emote_chance': 10,
        'combo_chance': 75,
        'highlight_chance': 5,
        'typing_time': 1.5,
        'max_concurrent_messages': 4,
        'status': 'dnd',
        'sleep': 'no',
        'quit_phrases': ''
    }

    bot_2 = ''
    config[bot_2] = {
        'name': bot_2,
        'messages': DATA_DIR + bot_2 + '_msg.txt',
        'channel': '',
        'emotes': '',
        'token': '',
        'sleep_time': 60,
        'emote_chance': 10,
        'combo_chance': 75,
        'highlight_chance': 5,
        'typing_time': 1.5,
        'max_concurrent_messages': 4,
        'status': 'online',
        'sleep': 'yes',
        'quit_phrases': ''
    }

    try:
        with open(DATA_DIR + 'config.ini', 'w') as configfile:
            config.write(configfile)
    except:
        print('Error: Failed to write configuration file.')
        sys.exit(1)


def load_config():
    config = configparser.ConfigParser()
    config_file = DATA_DIR + 'config.ini'

    try:
        config.read(config_file)
    except:
        print('Error: Failed to open configuration file.')
        sys.exit(1)

    return config
