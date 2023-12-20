#!/usr/bin/env python
# coding=utf-8

import requests
import os
import sys

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..'))
VERSION_INI_PATH = os.path.join(PROJECT_PATH, 'version.ini')


def get_version():
    # get global, major, minor versions from version.ini
    version_file = VERSION_INI_PATH
    with open(version_file, 'r') as f:
        lines = f.readlines()

    major = lines[0].split('=')[1].strip()
    minor = lines[1].split('=')[1].strip()
    patch = lines[2].split('=')[1].strip()

    return '%s.%s.%s' % (major, minor, patch)


def build_github_url(path, endpoint='api'):
    return 'https://%s.github.com%s' % (endpoint, path)


def create_github_release(version, tag):
    url = build_github_url('/repos/$ORG/$REPO/releases')
    data = {
        'tag_name': tag,
        #'target_commitish': tag,
        'name': 'Release %s' % tag,
        'body': """See version history at $link""",
        'draft': True,
        'prerelease': False
    }
    access_token = sys.argv[1]
    headers = {
        'Authorization': 'token %' % access_token
    }

    r = requests.post(url, json=data, headers=headers)
    print r.text
    return r.json()

if __name__ == "__main__":
    version = get_version()
    tag_name = 'v%s' % version

    print 'Creating github release %s' % tag_name
    release = create_github_release(version, tag_name)

    print 'Successfully release %s' % tag_name
