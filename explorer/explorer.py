import json
import os

from .page import Page

from .directory import Directory


class Explorer:
    def __init__(self, root="content", url_root="/"):
        self.root = root
        self.url_root = url_root
        self.pages = {}
        self.directories = {}
        self.contents = self.explore(root, url_root)
        self.directories['/'] = Directory(self.contents, '/')

    def explore(self, root, url_root):
        if os.path.exists(root):
            files = os.listdir(root)
        else:
            raise Exception(f"Path not found: {root}")
        content = {}
        for file in files:
            if file.endswith(".json"):
                file_content = Explorer.read_file(root, file, url_root)
                content[file_content.endpoint] = file_content
                self.pages[file_content.endpoint] = file_content
            elif "." not in file:
                new_url_root = f"{url_root}{file.lower()}/"
                dir_contents = self.explore(f"{root}/{file}", new_url_root)
                new_dir = Directory(dir_contents, new_url_root)
                content[new_url_root] = new_dir
                self.directories[new_url_root] = new_dir
        return content

    @staticmethod
    def read_file(root, file_name, url_root):
        with open(f"{root}/{file_name}") as file:
            content = json.load(file)
        return Page(content, url_root, file_name)
