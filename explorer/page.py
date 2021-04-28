class Page:
    def __init__(self, content, file_name):
        self.content = content
        self.file_name = file_name
        self.type = content["type"]
        if file_name == "index.json":
            self.endpoint = ""
            if not content.get("metadata"):
                self.content["metadata"] = {
                    "endpoint": self.endpoint
                }
        elif content.get("metadata"):
            self.endpoint = content["metadata"].get("endpoint") or file_name.split('.')[0]
        else:
            self.endpoint = file_name.split('.')[0]
            self.content["metadata"] = {
                "endpoint": self.endpoint
            }
