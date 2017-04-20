#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import test

test.start('Import')

try:
    import replika
except ImportError:
    test.failed('Cannot import library!')

test.ok()
