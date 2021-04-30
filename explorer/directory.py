from .page import Page


class Directory:
    def __init__(self, contents, url_root):
        self.url_root = url_root
        self.contents = contents
        self.parent = False
        if self.contents.get(f"{self.url_root}"):
            self.hasPage = True
            self.page = contents[self.url_root]
        else:
            self.hasPage = False

        self.children = []
        self.child_pages = []
        for child in self.contents.values():
            if isinstance(child, Page):
                child.set_parent(self)
                self.children.append(child)
                self.child_pages.append(child)
            if isinstance(child, Directory):
                child.set_parent(self)
                self.children.append(child)
                if child.hasPage:
                    self.child_pages.append(child.page)
        self.child_pages.sort(key=lambda child: child.endpoint)

    def set_parent(self, parent):
        self.parent = parent
