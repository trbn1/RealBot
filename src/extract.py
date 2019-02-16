# -*- coding: utf-8 -*-

import config as cfg
import json
import re


def extract_messages():
    cfg.generate_config()
    config = cfg.load_config()

    with open(config.get('FilePaths', 'source_data'), 'r', encoding='utf8') as jdata:
        data = json.load(jdata)

    msg_list = []
    for channel in data['data']:
        for msg in data['data'][channel]:
            if data['data'][channel][msg]['u'] is int(config.get('Extract', 'user')):
                msg_list.append(data['data'][channel][msg]['m'])

    with open(config.get('FilePaths', 'source_messages'), 'w', encoding='utf8') as f:
        for item in msg_list:
            item = re.sub(r'[^ ]+\.[^ ]+[ ]{0,}|<(.*?)>+[ ]{0,}', '', item)
            if item is not '':
                f.write("%s\n" % item)

if __name__ == '__main__':
	extract_messages()
