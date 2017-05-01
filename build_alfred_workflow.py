#!/usr/bin/env python
# -*- encoding: utf-8

import collections
import os
import plistlib
import uuid
import zipfile

aws_region = 'eu-west-1'

data = {
    'bundleid': 'com.alexwlchan.aws-shortcuts',
    'category': 'Internet',
    'connections': {},
    'createdby': 'Alex Chan',
    'description': f'Shortcuts for the AWS console ({aws_region})',
    'name': 'AWS shortcuts',
    'objects': [],
    'readme': '',
    'uidata': {},
    'version': '0.0.1',
    'webaddress': 'https://github.com/alexwlchan/alfred-aws-shortcuts',
}

aws_resources = sorted([
    f[:-len('.png')]
    for f in os.listdir('AWS shortcuts')
    if f.endswith('.png')
])

for idx, resource in enumerate(aws_resources):
    trigger_object = {
        'config': {
            'argumenttype': 2,
            'keyword': resource.lower(),
            'subtext': '',
            'text': resource,
            'withspace': False,
        },
        'type': 'alfred.workflow.input.keyword',
        'uid': str(uuid.uuid4()).upper(),
        'version': 1,
    }

    browser_object = {
        'config': {
            'browser': '',
            'spaces': '',
            'url': f'https://{aws_region}.console.aws.amazon.com/{resource}',
            'utf8': True,
        },
        'type': 'alfred.workflow.action.openurl',
        'uid': str(uuid.uuid4()).upper(),
        'version': 1,
    }

    data['objects'].append(trigger_object)
    data['objects'].append(browser_object)

    data['uidata'][trigger_object['uid']] = {
        'xpos': 50 + (400 * (idx % 2)),
        'ypos': 50 + 300 * (2 * idx % 2),
    }
    data['uidata'][browser_object['uid']] = {
        'xpos': 250 + (400 * (idx % 2)),
        'ypos': 50 + 300 * (2 * idx % 2),
    }

    data['connections'][trigger_object['uid']] = [
        {
            'destinationuid': browser_object['uid'],
            'modifiers': 0,
            'modifiersubtext': '',
            'vitoclose': False,
        }
    ]


os.chdir('AWS shortcuts')
plistlib.writePlist(data, 'info.plist')

os.unlink('../AWS shortcuts.alfredworkflow')
with zipfile.ZipFile('../AWS shortcuts.alfredworkflow', 'w') as package:

    for filename in os.listdir('.'):
        if filename.startswith('.'):
            continue
        package.write(filename)
