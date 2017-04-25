#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
import logging
import traceback
logging.basicConfig(level=logging.DEBUG)

ENABLE_QUIT = True
_test_name = 'unknown'

class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def start(test_name):
    global _test_name
    logging.info('[START] Test: %s' % test_name)
    _test_name = test_name
    

def _end(quit=False, code=0):
    if quit:
        sys.exit(code)

def ok(message=None):
    msg = '' if message is None else (' (%s)' % message)
    logging.info('[PASS ]%s' % msg)
    _end()

def failed(message, fail_code=-1):
    logging.warning('[FAIL ] %s' % message)
    print color.FAIL
    traceback.print_exc()
    print color.ENDC
    _end(ENABLE_QUIT, fail_code)

if __name__ == '__main__':    
    logging.info('Run all tests...')

    import glob

    python_files = set(glob.glob('*.py'))
    excludes = set(glob.glob('_*.py') + ['test.py'])
    test_programs = list(python_files - excludes)
    test_programs.sort()
        
    for program in test_programs:
        execfile(program)
        
    logging.info('Bye.')
