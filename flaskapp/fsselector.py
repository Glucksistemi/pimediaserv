import os
from config import CONTENT_PATHS
import json # temporary for testing

full_content_paths = CONTENT_PATHS # for future flash card mounting


def get_full_path(root, path):
    try:
        return os.path.join(full_content_paths[int(root)]['path'],path)
    except IndexError:
        return ''


def get_roots():
    rt = []
    for root in full_content_paths:
        rt.append(root['name'])
    return rt


def get_folder_contents(root, folder):
    path = get_full_path(root, folder)
    if not path:
        return {'error': True, 'error_data': 'index error: wrong path or forbidden root folder'}
    rt = {
        'folders': [],
        'files': []
    }
    for item in os.listdir(path): # TODO: add symlink and mount points support
        if os.path.isfile(os.path.join(path, item)):
            rt['files'].append(item)
        elif os.path.isdir(os.path.join(path, item)):
            rt['folders'].append(item)
    return rt


