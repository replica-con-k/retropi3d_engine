#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import test

test.start('Imports')

try:
    import replika
    import replika.assets
    import replika.ingame

except ImportError:
    test.failed('Cannot import library and modules!')

test.ok()
