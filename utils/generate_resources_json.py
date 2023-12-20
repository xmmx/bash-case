#!/usr/bin/python

# PLACED in /apps/utility/
# This script generates resources.json file.
# Called by /apps/utility/themes_locales_geodata_dist.sh

import os
import sys
import traceback
import json
import re

# generate_resources_json.py /apps/static/cdn/releases/8.5.0
ROOT_PATH = os.path.abspath(sys.argv[1])
RESOURCES_JSON_PATH = os.path.abspath(os.path.join(ROOT_PATH, 'resources.json'))

def build_fonts():
    fonts_path = os.path.join(ROOT_PATH, 'fonts')
    rv = {}
    for (path, dirs, files) in os.walk(fonts_path):
        files_list = []
        if 'demos' in path:
            continue
        dir_name = path.rsplit('/', 1)[-1]

        for file_name in files:
            files_list.append({'name': file_name})

        rv[dir_name] = files_list
 
    return rv

def build_modules():
    builded_modules_path = os.path.join(ROOT_PATH, 'js', 'modules.json')
    with open(builded_modules_path, 'r') as f:
        rv = json.load(f)
        f.close()
    return rv

def build_themes():
    with open(RESOURCES_JSON_PATH, 'r') as f:
        resources_json = json.load(f)
        f.close()
    return resources_json['themes']

def build_css():
    css_path = os.path.join(ROOT_PATH, 'css')
    rv = []
    for (path, dirs, files) in os.walk(css_path):
        for file_name in files:
            rv.append({'name': file_name})

    return rv

def build_geodata():
    geodata_path = os.path.join(ROOT_PATH, 'geodata')
    rv = {}

    for (path, dirs, files) in os.walk(geodata_path):
        rel_path = os.path.relpath(path, geodata_path)
        split = rel_path.split('/')

        if not split[-1] + '.js' in files:
            continue

        target = rv
        for item in split:
            if not item in target:
                target[item] = {}
            target = target[item]
            if item == split[-1]:
                name_parts = item.split('_')
                name_parts = map(lambda x: x.capitalize(), name_parts)
                target['name'] = ' '.join(name_parts)

    return rv

def build_locales():
    locales_path = os.path.join(ROOT_PATH, 'locales')
    rv = {}
    for (path, dirs, files) in os.walk(locales_path):
        for file_name in files:
            locale_path = os.path.join(path, file_name)
            f = open(locale_path, 'r')
            text = f.read()
            f.close()

            code = re.search("code: ['\"](.+)['\"],", text, re.IGNORECASE).group(1)
            eng_name = re.search("engName: ['\"](.+)['\"],", text, re.IGNORECASE).group(1)
            native_name = re.search("nativeName: ['\"](.+)['\"],", text, re.IGNORECASE).group(1)

            rv[code] = {'eng-name': eng_name, 'native-name': native_name}

    return rv

def main():
    resources_json = {}

    resources_json['fonts'] = build_fonts()
    resources_json['modules'] = build_modules()
    resources_json['themes'] = build_themes()
    resources_json['css'] = build_css()
    resources_json['geodata'] = build_geodata()
    resources_json['locales'] = build_locales()

    with open(RESOURCES_JSON_PATH, 'w') as f:
        f.write(json.dumps(resources_json))
        f.close()

if __name__ == '__main__':
    try:
        main()
    except (StandardError, KeyboardInterrupt):
        print traceback.format_exc()
        sys.exit(1)
