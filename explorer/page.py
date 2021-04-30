from .utils import slugify


class Page:
    def __init__(self, content, url_root, file_name):
        self.content = content
        self.file_name = file_name
        self.type = content["type"]
        self.parent = False

        # get endpoint termination + ensure metadata exists
        if content.get("metadata"):
            endpoint_termination = content["metadata"].get("endpoint") or file_name.lower().split('.')[0]
        else:
            endpoint_termination = file_name.split('.')[0]
            self.content["metadata"] = {}
        endpoint_termination = f"/{slugify(endpoint_termination)}"

        if file_name == "index.json":
            endpoint_termination = ""
            if url_root == "":
                endpoint_termination = "/"

        self.endpoint = f"{url_root}{endpoint_termination}"
        self.content["metadata"]["endpoint"] = self.endpoint
        self.metadata = self.content["metadata"]

    def set_parent(self, parent):
        self.parent = parent

    @property
    def endpoint_name(self):
        return self.endpoint[1:].replace("/", "_")
