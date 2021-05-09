import os


def use_sm(text):
    return "_sm.".join(text.rsplit(".", 1))


def process(root, file_name):
    unix_filename = f"{root}/{file_name}".replace(" ", "\ ")
    new_filename = use_sm(unix_filename)
    os.system(f"convert {unix_filename} -resize 650x490 {new_filename}")


def explore(root):
    if os.path.exists(root):
        files = os.listdir(root)
    else:
        raise Exception(f"Path not found: {root}")

    for file in files:
        if file.lower().endswith(".jpg") and not file.lower().endswith("_sm.jpg"):
            process(root, file)
        elif "." not in file:
            explore(f"{root}/{file}")


explore("../static/media/Photos site")
