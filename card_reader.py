import hashlib
import json
import os

def gen_uid(question):
    text = question["title"] + "---" + question["solution"]
    return hashlib.md5(text.encode("UTF8")).hexdigest()

def read_folder(path):
    data = []

    for name in os.listdir(path):
        sub_path = os.path.join(path, name)
        if os.path.isdir(sub_path):
            data += read_folder(sub_path)
        else:
            data += read_file(sub_path)
    
    return data

def read_file(path):
    with open(path, "r") as f:
        data = json.load(f)
    
    generated = False
    for question in data:
        if "guid" not in question:
            question["guid"] = gen_uid(question)
            generated = True
    
    if generated:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    return data

data = read_folder("subjects")
