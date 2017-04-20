#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
import logging
logging.basicConfig(level=logging.INFO)

ENABLE_QUIT = True
_test_name = 'unknown'

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
