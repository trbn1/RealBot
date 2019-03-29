# -*- coding: utf-8 -*-

import config as cfg
import re
import sys
from multiprocessing import Pool


def postprocess_messages(name):
    cfg.generate_training_config(name)
    config = cfg.load_config(name + '/')

    try:
        with open(config.get('FilePaths', 'generated_messages'), 'r', encoding='utf8') as f:
            messages = f.readlines()
    except:
        print('Error: Failed to open %s.' % config.get('FilePaths', 'generated_messages'))
        sys.exit(1)

    proper_messages = []
    for item in messages:
        # uppercase
        if re.match(r'^xd', item):
            item = item.upper()
        if 'xd' in item:
            item = re.sub(r'(xd{1,})', 'XD', item)

        # remove space after character
        if re.match(r'(^\.\s)', item):
            item = re.sub(r'(^\.\s)', '.', item)
        if re.match(r'(^\,\s)', item):
            item = re.sub(r'(^\,\s)', ',', item)
        if '$ ' in item:
            item = re.sub(r'(^\$\s)+', '$', item)
        if '! ' in item:
            item = re.sub(r'(\!\s)+', '!', item)
        if ': ' in item:
            item = re.sub(r'(\:\s)+', ':', item)
        if '; ' in item:
            item = re.sub(r'(\;\s)+', ';', item)
        if '- ' in item:
            item = re.sub(r'(\-\s)+', '-', item)
        if '+ ' in item:
            item = re.sub(r'(\+\s)+', '+', item)
        if '< ' in item:
            item = re.sub(r'(\<\s)+', '<', item)
        if '> ' in item:
            item = re.sub(r'(\>\s)+', '>', item)
        if '^ ' in item:
            item = re.sub(r'(\^\s)+', '^', item)
        if '[ ' in item:
            item = re.sub(r'(\[\s)+', '[', item)
        if '* ' in item:
            item = re.sub(r'(\*\s)+', '*', item)
        if '@ ' in item:
            item = re.sub(r'(\@\s)+', '@', item)
        if '# ' in item:
            item = re.sub(r'(\#\s)+', '#', item)
        if '_ ' in item:
            item = re.sub(r'(\_\s)+', '_', item)
        if '( ' in item:
            item = re.sub(r'(\(\s)+', '(', item)
        if '~ ' in item:
            item = re.sub(r'(\~\s)+', '~', item)
        if '= ' in item:
            item = re.sub(r'(\=\s)+', '=', item)
        if ' \' ' in item:
            item = re.sub(r'(\s\'\s)+', '\'', item)
        if ' \" ' in item:
            item = re.sub(r'(\s\"\s)+', '\"', item)
        if '\' ' in item:
            item = re.sub(r'(\'\s)+', '\'', item) 
        if '\" ' in item:
            item = re.sub(r'(\"\s)+', '\"', item) 
        if '/ ' in item:
            item = re.sub(r'(\/\s)+', '/', item)

        # remove space before character
        if ' /' in item:
            item = re.sub(r'(\s\/)+', '/', item) 
        if ' ?' in item:
            item = re.sub(r'(\s\?)+', '?', item)
        if ' !' in item:
            item = re.sub(r'(\s\!)+', '!', item)
        if ' ,' in item:
            item = re.sub(r'(\s\,)+', ',', item)
        if ' .' in item:
            item = re.sub(r'(\s\.)+', '.', item)
        if ' )' in item:
            item = re.sub(r'(\s\))+', ')', item)
        if ' \'' in item:
            item = re.sub(r'(\s\')+', '\'', item) 
        if ' -' in item:
            item = re.sub(r'(\s\-)+', '-', item)
        if ' :' in item:
            item = re.sub(r'(\s\:)+', ':', item)
        if ' ;' in item:
            item = re.sub(r'(\s\;)+', ';', item)
        if ' ]' in item:
            item = re.sub(r'(\s\])+', ']', item)
        if ' $' in item:
            item = re.sub(r'(\s\$)+', '$', item)
        if ' %' in item:
            item = re.sub(r'(\s\%)+', '%', item)
        if ' =' in item:
            item = re.sub(r'(\s\=)+', '=', item)
        if ' _' in item:
            item = re.sub(r'(\s\_)+', '', item)

        # empty line
        if item is '':
            continue

        # line length
        if len(item) > 100 or len(item) < 3:
            continue

        # line starts/ends with
        if item.startswith(('$', '.', ',', '[', ']', 'pulltop', ' ', 'k !', 't !', '^', '`',
                            '!', '%', '\"', '\\', '/', '\'', '-', '~', '*', ':+', '+', '|',
                            ')', ';\"', '? ', '#', '@ ', '(^', '{', '}', '=')):
            continue
        if item.endswith(('*', '#', '@', ',', '`', '=', ':-', ':+')):
            continue

        # unwanted strings
        if '@someone' in item:
            continue
        if re.match(r'^;[A-z]*', item):
            continue
        if re.match(r'^:[A-z]*', item):
            continue
        if re.match(r'^([A-z]\.).*', item):
            continue
        if re.match(r'^([A-z]\,).*', item):
            continue
        if re.match(r'^([A-z]\").*', item):
            continue
        if re.match(r'.*\".*\".*\".*', item):
            continue
        if re.match(r'.*\,.*\,.*\,.*', item):
            continue
        if re.match(r'.*\..*\..*\..*\..*', item):
            continue

        proper_messages.append(item)
    
    try:
        with open(config.get('FilePaths', 'messages'), 'w', encoding='utf8') as f:
            f.write(''.join(proper_messages))
    except:
        print('Error: Failed to write %s.' % config.get('FilePaths', 'generated_messages'))
        sys.exit(1)


if __name__ == '__main__':
    cfg.generate_bot_config()
    bot_config = cfg.load_config()
    names = []
    for section in bot_config.sections():
        names.append(bot_config.get(section, 'name'))

    pool = Pool()
    pool.map(postprocess_messages, names)
    pool.close()
    pool.join()	
