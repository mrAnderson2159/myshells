import json
import os
import re
import sys
import datetime

from xattr import xattr
from colors import cyan
from utils import clear
from typing import *


def get_package() -> dict:
    # 𝚯(1)
    with open(os.path.join(sys.argv[0], 'package.json'), 'r') as s:
        return json.loads(s.read())


def write_package(package: dict):
    with open(os.path.join(sys.argv[0], 'package.json'), 'w') as s:
        s.write(json.dumps(package))


def get_today():
    t = datetime.datetime.now()
    return [t.day, t.month, t.year]

def feature(name: str) -> None:
    clear()
    cyan(f"University Manager - {name}\n")


def match(s: str, rgx) -> Optional[re.Match]:
    # 𝚯(1)
    match = re.match(rgx, s)
    return match.groups() if match else None


def get_videos(folder: str, rgx=None) -> list:
    # O(videos in folder)
    rgx = rgx if rgx else r'^(\d{4}-\d{2}-\d{2})[\s_]+(\d{2}-\d{2}-\d{2})\.(mp4|mkv)$'
    res = list()
    for video in os.listdir(folder):
        m = match(video, rgx)
        if m:
            res.append((video, m))
    return res


def get_tag(file: str) -> str:
    colornames = ['none', 'gray', 'green', 'purple', 'blue', 'yellow', 'red', 'orange']
    attrs = xattr(file)

    try:
        finder_attrs = attrs['com.apple.FinderInfo']
        color = finder_attrs[9] >> 1 & 7
    except KeyError:
        color = 0

    return colornames[color]


def set_tag(file: str, tag: str) -> None:
    feature("Set Tag")

    def set_label(filename, color_name):
        if get_tag(filename) != 'none' and color_name != 'none':
            set_label(filename, 'none')
        colors = ['none', 'gray', 'green', 'purple', 'blue', 'yellow', 'red', 'orange']
        key = u'com.apple.FinderInfo'
        attrs = xattr(filename)
        current = attrs.copy().get(key, chr(0) * 32)
        try:
            changed = current[:9] + chr(colors.index(color_name) * 2) + current[10:]
            attrs.set(key, changed.encode())
        except TypeError:
            changed = current[:9] + chr(colors.index(color_name) * 2).encode() + current[10:]
            attrs.set(key, changed)
        cyan(f"{file} tagged '{color_name}'\n")

    if tag not in ('done', 'start', 'todo'):
        raise ValueError(f'Tag può essere "done", "start", "todo", non {tag}')
    if tag == 'done':
        set_label(file, 'green')
    elif tag == 'start':
        set_label(file, 'yellow')
    else:
        set_label(file, 'red')


# def generate_random_video_titles_for_testing():
#     from random import randint
#     az = lambda n: f'0{n}' if len(str(n)) == 1 else str(n)
#     h = '09', '11', '14', '16'
#     for i in range(len(h)):
#         if not i % 2:
#             for j in range(2):
#                 print(f'2022-03-16 {h[i]}-{az(randint(0, 59))}-30.{["mkv", "mp4"][randint(0, 1)]}')
