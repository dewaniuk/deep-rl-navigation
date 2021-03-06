#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import inspect
import logging
import zipfile
import platform

from unityagents import UnityEnvironment

try:
    from IPython.display import Markdown, display
except Exception:
    logging.exception('Failed to import jupyter modules. Ignoring')

here = os.path.dirname(os.path.abspath(__file__))


def build_environment(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        zipped = directory + '.zip'
        if os.path.exists(zipped):
            with zipfile.PyZipFile(zipped) as zfp:
                logging.info('Extracting environment...')
                zfp.extractall()
        else:
            raise Exception('Unable to proceed. Cannot find environment.')
    os.chmod(path, 0o755)
    return UnityEnvironment(file_name=path)

def get_executable_path():
    parent = os.path.dirname(here)
    if platform.system() == 'Linux':
        if '64' in platform.architecture()[0]:
            return os.path.join(parent, 'Banana_Linux', 'Banana.x86_64')
        else:
            return os.path.join(parent, 'Banana_Linux', 'Banana.x86')
    elif platform.system() == 'Darwin':
            return os.path.join(parent, 'Banana.app')
    elif platform.system() == 'Windows':
        if '64' in platform.architecture()[0]:
            return os.path.join(parent, 'Banana_Windows_x86_64', 'Banana.exe')
        else:
            return os.path.join(parent, 'Banana_Windows_x86', 'Banana.exe')
    else:
        logging.error('Unsupported platform!')
        raise ValueError('Unsupported platform')

def print_source(obj):
    source = inspect.getsource(obj)
    display(Markdown('```python\n' + source + '\n```'))

def load_environment():
    path = get_executable_path()
    return build_environment(path)
