import csv
import json
import os

infos = {}
with open('/home/marie-sophie/work/ims-nature/Taxonomie_mammiferes.csv', newline='', encoding='utf8') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for line in csv_reader:
        infos[line["Espèce"]] = line


def process(root, file_name):
    with open(f"{root}/{file_name}", encoding="utf8") as file:
        content = json.load(file)
    try:
        info = infos.pop(content["name"])
        content["taxonomy"] = info
        with open(f"{root}/{file_name}", "w", encoding='utf8') as file:
            json.dump(content, file, indent=2, ensure_ascii=False)
    except Exception as e:
        print(file_name)


def explore(root):
    if os.path.exists(root):
        files = os.listdir(root)
    else:
        raise Exception(f"Path not found: {root}")

    for file in files:
        if file.endswith(".json"):
            process(root, file)
        elif "." not in file:
            explore(f"{root}/{file}")


explore("../content/Mammifères")
print(infos)
