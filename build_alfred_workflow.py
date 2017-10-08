#!/usr/bin/env python3
# -*- encoding: utf-8

import os
import plistlib
import shutil
import tempfile
import uuid

from PIL import Image
import yaml


def build_alfred_workflow(src_dir, name):
    """
    Given a directory of source files for an Alfred Workflow, assemble them
    into a .alfredworkflow bundle and return its path.
    """
    shutil.make_archive(
        base_name=f'{name}.alfredworkflow',
        format='zip',
        root_dir=src_dir
    )
    shutil.move(f'{name}.alfredworkflow.zip', f'{name}.alfredworkflow')
    return f'{name}.alfredworkflow'


def load_initial_data(yaml_data):
    """
    Given some YAML metadata, build the package-level metadata dict.
    """
    defaults = {
        'bundleid': 'edu.self.alfred-shortcuts',
        'category': 'Internet',
        'connections': {},
        'createdby': '',
        'description': 'Shortcut links for Alfred',
        'name': 'Alfred shortcuts',
        'objects': [],
        'readme': '',
        'uidata': {},
        'version': '0.0.1',
        'webaddress': 'https://github.com/alexwlchan/alfred-shortcuts',
    }

    return {
        key: yaml_data.get(key, defaults[key]) for key in defaults
    }


aws_region = 'eu-west-1'

yaml_data = yaml.load(open('alfred-shortcuts.yml'))
data = load_initial_data(yaml_data)

t_dir = tempfile.mkdtemp()

for idx, shortcut_data in enumerate(yaml_data.get('shortcuts')):
    shortcut = shortcut_data['shortcut']
    url = shortcut_data['url']
    title = shortcut_data['title']

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

    icon = os.path.join('icons', shortcut_data['icon'])
    resized = os.path.join(t_dir, f'{trigger_object["uid"]}.png')
    if not os.path.exists(resized):
        base_icon = Image.open(icon)
        width, height = base_icon.size
        if width == height:
            shutil.copyfile(icon, resized)
        elif width > height:
            new = Image.new('RGBA', (width, width))
            new.paste(base_icon, (0, (width - height) // 2), base_icon)
            new.save(resized)
        else:
            new = Image.new('RGBA', (height, height))
            new.paste(base_icon, ((height - width) // 2, 0), base_icon)
            new.save(resized)

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

build_alfred_workflow(src_dir=t_dir, name='shortcuts')
