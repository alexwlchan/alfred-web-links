#!/usr/bin/env python
# -*- encoding: utf-8

import collections
import os
import plistlib
import shutil
import tempfile
import uuid
import zipfile

from PIL import Image

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

names = {
    'EMR': {
        'title': 'Elastic MapReduce',
        'slug': 'elasticmapreduce',
    },
    'ES': {
        'title': 'Elasticsearch Service',
    },
    'AppStream': {
        'slug': 'appstream2',
    },
    'ECS': {
        'title': 'EC2 Container Service',
    },
    'ECR': {
        'title': 'EC2 Container Registry',
    },
}

t_dir = tempfile.mkdtemp()

for idx, resource in enumerate(aws_resources):

    shortcut = names.get(resource, {}).get('shortcut', resource.lower())
    slug = names.get(resource, {}).get('slug', resource.lower())
    url = f'https://{aws_region}.console.aws.amazon.com/{slug}'
    if resource == 'ECR':
        url = 'https://{aws_region}.console.aws.amazon.com/ecs/home?region=eu-west-1#/repositories'
    title = names.get(resource, {}).get('title', resource)

    trigger_object = {
        'config': {
            'argumenttype': 2,
            'keyword': shortcut,
            'subtext': '',
            'text': title,
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
            'url': url,
            'utf8': True,
        },
        'type': 'alfred.workflow.action.openurl',
        'uid': str(uuid.uuid4()).upper(),
        'version': 1,
    }

    if not os.path.exists(os.path.join('AWS shortcuts', f'{resource}_resized.png')):
        base_icon = Image.open(os.path.join('AWS shortcuts', f'{resource}.png'))
        width, height = base_icon.size
        if width == height:
            shutil.copyfile(
                os.path.join('AWS shortcuts', f'{resource}.png'),
                os.path.join('AWS shortcuts', f'{resource}_resized.png')
            )
        elif width > height:
            new = Image.new('RGBA', (width, width))
            new.paste(base_icon, (0, (width - height) // 2), base_icon)
            new.save(os.path.join('AWS shortcuts', f'{resource}_resized.png'))
        else:
            new = Image.new('RGBA', (height, height))
            new.paste(base_icon, ((height - width) // 2, 0), base_icon)
            new.save(os.path.join('AWS shortcuts', f'{resource}_resized.png'))
        # assert False

    shutil.copyfile(
        os.path.join('AWS shortcuts', f'{resource}_resized.png'),
        os.path.join(t_dir, f'{trigger_object["uid"]}.png')
    )

    data['objects'].append(trigger_object)
    data['objects'].append(browser_object)

    data['uidata'][trigger_object['uid']] = {
        'xpos': 50 + (400 * (idx % 2)),
        'ypos': 50 + 75 * (idx - idx % 2),
    }
    data['uidata'][browser_object['uid']] = {
        'xpos': 250 + (400 * (idx % 2)),
        'ypos': 50 + 75 * (idx - idx % 2),
    }

    data['connections'][trigger_object['uid']] = [
        {
            'destinationuid': browser_object['uid'],
            'modifiers': 0,
            'modifiersubtext': '',
            'vitoclose': False,
        }
    ]

shutil.copyfile('AWS-icon.png', os.path.join(t_dir, 'Icon.png'))
plistlib.writePlist(data, os.path.join(t_dir, 'info.plist'))

try:
    os.unlink('AWS shortcuts.alfredworkflow')
except FileNotFoundError:
    pass

with zipfile.ZipFile('AWS shortcuts.alfredworkflow', 'w') as package:
    os.chdir(t_dir)
    for filename in os.listdir('.'):
        if filename.startswith('.'):
            continue
        package.write(filename)
