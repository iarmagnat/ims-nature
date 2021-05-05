import json
import os
from collections import defaultdict
from .page import Page
from .directory import Directory
from .utils import slugify


def page_factory():
    return Page


class Explorer:
    def __init__(self, root="content", url_root="", page_types={}):
        # todo: check if all page_types ar of type Page
        self.page_types = defaultdict(page_factory, **page_types)
        self.root = root
        self.url_root = slugify(url_root)
        self.pages = {}
        self.directories = {}
        self.contents = self.explore(self.root, self.url_root)
        self.directories[f"/{self.url_root}"] = Directory(self.contents, f"/{self.url_root}")

    def explore(self, root, url_root):
        if os.path.exists(root):
            files = os.listdir(root)
        else:
            raise Exception(f"Path not found: {root}")
        content = {}
        for file in files:
            if file.endswith(".json"):
                page = self.read_file(root, file, url_root)
                content[page.endpoint] = page
                self.pages[page.endpoint] = page
            elif "." not in file:
                new_url_root = f"{url_root}/{slugify(file)}"
                dir_contents = self.explore(f"{root}/{file}", new_url_root)
                new_dir = Directory(dir_contents, new_url_root)
                content[new_url_root] = new_dir
                self.directories[new_url_root] = new_dir
        return content

    def read_file(self, root, file_name, url_root):
        with open(f"{root}/{file_name}") as file:
            content = json.load(file)
        return self.page_types[content["type"]](content, url_root, file_name)

    @property
    def root_pages(self):
        return self.directories[f"/{self.url_root}"].child_pages
