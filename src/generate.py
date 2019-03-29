# -*- coding: utf-8 -*-

import config as cfg

from textgenrnn import textgenrnn


def generate_messages(name):
    cfg.generate_training_config(name)
    config = cfg.load_config()

    textgen = textgenrnn(config.get('Model', 'weights'),
                        config.get('Model', 'vocab'),
                        config.get('Model', 'config'))
    generated = textgen.generate(n=int(config.get('Model', 'generated_lines')), temperature=1, return_as_list=True)

    with open(config.get('FilePaths', 'generated_messages'), 'w', encoding='utf8') as f:
        for item in generated:
            if item is not '':
                f.write(item + '\n')
				
				
if __name__ == '__main__':
	generate_messages('')
