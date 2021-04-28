import json
import os

from .page import Page


def explore(root="content", url_root="/"):
    if os.path.exists(root):
        files = os.listdir(root)
    else:
        raise Exception(f"Path not found: {root}")
    content = {}
    for file in files:
        if "." in file:
            file_content = read_file(root, file)
            endpoint = file_content.endpoint
            content[endpoint] = file_content
        else:
            new_url_root = f"{url_root}{file.lower()}/"
            content[new_url_root] = explore(f"{root}/{file}", new_url_root)
    return content


def read_file(root, file_name):
    with open(f"{root}/{file_name}") as file:
        content = json.load(file)
    return Page(content, file_name)
