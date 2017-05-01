#!/usr/bin/env python
# -*- encoding: utf-8

import os
import plistlib
import zipfile

with zipfile.ZipFile('AWS shortcuts.alfredworkflow', 'w') as package:
    os.chdir('AWS shortcuts')
    for filename in os.listdir('.'):
        if filename.startswith('.'):
            continue
        package.write(filename)

data = {
    'bundleid': 'com.alexwlchan.example',
    'category': 'Tools/Internet/Productivity/Uncategorised',
    'createdby': 'Alex Chan',
    'description': 'An example workflow',
    'name': 'Example',
    'readme': 'The README goes here',
    'version': '0.0.1',
    'webaddress': 'https://example.com',
}

plistlib.writePlist(data, 'info.plist')