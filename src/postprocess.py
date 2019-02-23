# -*- coding: utf-8 -*-

import config as cfg
import re
import sys


def postprocess_messages():
    cfg.generate_config()
    config = cfg.load_config()

    try:
        with open(config.get('FilePaths', 'generated_messages'), 'r', encoding='utf8') as f:
            messages = f.readlines()
    except:
        print('Error: Failed to open %s.' % config.get('FilePaths', 'generated_messages'))
        sys.exit(1)

    try:
        with open(config.get('FilePaths', 'messages'), 'w', encoding='utf8') as f:
            for item in messages:
                if re.match(r'^xd', item):
                    item = item.upper()
                if 'xd' in item:
                    item = re.sub(r'(xd{1,})', 'XD', item)
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
                if ' /' in item:
                    item = re.sub(r'(\s\/)+', '/', item) 
                if ' ?' in item:
                    item = re.sub(r'(\s\?)+', '?', item)
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
                if item is not '' and len(item) < 100:
                    f.write('%s' % item)
    except:
        print('Error: Failed to write %s.' % config.get('FilePaths', 'generated_messages'))
        sys.exit(1)


if __name__ == '__main__':
	postprocess_messages()
