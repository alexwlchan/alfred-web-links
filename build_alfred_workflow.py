#!/usr/bin/env python
# -*- encoding: utf-8

import os
import zipfile

with zipfile.ZipFile('AWS shortcuts.alfredworkflow', 'w') as package:
    os.chdir('AWS shortcuts')
    for filename in os.listdir('.'):
        if filename.startswith('.'):
            continue
        package.write(filename)
