import hashlib
import json
import os

from consts import EXPLANATION_SUFFIX, DRAWING_SUFFIX

def gen_uid(question):
    data = json.dumps(question, indent=2)
    return hashlib.md5(data.encode("UTF8")).hexdigest()

def read_folder(path, names):
    data = []

    for name in os.listdir(path):
        display_name = name
        if "." in display_name:
            display_name = name[:name.index(".")]
        new_names = list(names)
        new_names.append(display_name)
        
        sub_path = os.path.join(path, name)
        if os.path.isdir(sub_path):
            data += read_folder(sub_path, new_names)
        else:
            data += read_file(sub_path, new_names)
    
    return data

def read_file(path, new_names):
    if path.endswith(".json"):
        cards = read_json(path)
    if path.endswith(".tikz"):
        cards = read_tikz(path)
    
    for card in cards:
        card["tags"] = new_names
        
    return cards
    
def read_tikz(path):
    with open(path, "r") as f:
        data = f.readlines()
    
    title = data[0].strip()
    uid = data[1].strip()
    text_answer = data[2].strip()
    tikz = "".join(data[3:])
    
    cards = [
        {
            "title": f"{title} tikz Erklärung",
            "solution": text_answer,
            "guid": f"{uid}.{EXPLANATION_SUFFIX}"
        },
        {
            "title": f"{title} tikz Darstellung",
            "solution_latex": tikz,
            "guid": f"{uid}.{DRAWING_SUFFIX}",
            "latex_env": "tikz"
        },
    ]
    
    return cards
    
def read_json(path):
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
