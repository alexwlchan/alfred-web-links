#!/usr/bin/env python3
# -*- encoding: utf-8

import os
import plistlib
import shutil
import tempfile
import uuid

from PIL import Image
import yaml


class AlfredWorkflow:

    def __init__(self, path):
        self.path = path
        self.yaml_data = yaml.load(open(path))
        self.tmpdir = tempfile.mkdtemp()
        self.metadata = {}

    def tmpfile(self, path):
        return os.path.join(self.tmpdir, path)

    def build(self, name):
        self.metadata = self._get_package_metadata()

        for idx, link_data in enumerate(self.yaml_data['links']):
            self._add_link(idx=idx, link_data=link_data)

        self._copy_workflow_icon()
        plistlib.writePlist(self.metadata, self.tmpfile('Info.plist'))
        self._build_alfred_workflow_zip(name=name)

    def _copy_workflow_icon(self):
        try:
            icon = self.yaml_data['icon']
        except KeyError:
            pass
        else:
            icon_path = os.path.join('icons', icon)
            shutil.copyfile(icon_path, self.tmpfile('Icon.png'))

    def _get_package_metadata(self):
        defaults = {
            'bundleid': 'edu.self.alfred-web-links',
            'category': 'Internet',
            'connections': {},
            'createdby': '',
            'description': 'Web links links for Alfred',
            'name': 'Alfred web links',
            'objects': [],
            'readme': '',
            'uidata': {},
            'version': '0.0.1',
            'webaddress': 'https://github.com/alexwlchan/alfred-web-links',
        }

        return {
            key: self.yaml_data.get(key, defaults[key]) for key in defaults
        }

    def _add_link(self, idx, link_data):
        shortcut = link_data['shortcut']
        url = link_data['url']
        title = link_data['title']

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

        icon = os.path.join('icons', link_data['icon'])
        resized = self.tmpfile(f'{trigger_object["uid"]}.png')
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

        self.metadata['objects'].append(trigger_object)
        self.metadata['objects'].append(browser_object)

        self.metadata['uidata'][trigger_object['uid']] = {
            'xpos': 150,
            'ypos': 50 + 120 * idx,
        }
        self.metadata['uidata'][browser_object['uid']] = {
            'xpos': 600,
            'ypos': 50 + 120 * idx,
        }

        self.metadata['connections'][trigger_object['uid']] = [
            {
                'destinationuid': browser_object['uid'],
                'modifiers': 0,
                'modifiersubtext': '',
                'vitoclose': False,
            }
        ]

    def _build_alfred_workflow_zip(self, name):
        """
        Given a directory of source files for an Alfred Workflow, assemble them
        into a .alfredworkflow bundle.
        """
        shutil.make_archive(
            base_name=f'{name}.alfredworkflow',
            format='zip',
            root_dir=self.tmpdir
        )
        shutil.move(f'{name}.alfredworkflow.zip', f'{name}.alfredworkflow')


if __name__ == '__main__':
    workflow = AlfredWorkflow(path='alfred-web-links.yml')
    workflow.build(name='web-links')
