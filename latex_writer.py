import os
import subprocess
from tqdm import tqdm
from consts import ANSWER, SOLUTION

workspace_folder = os.path.abspath("workspace")
tex_file = os.path.join(workspace_folder, "main.tex")
dvi_file = os.path.join(workspace_folder, "main.dvi")

with open("template.tex", "r") as f:
    template = f.read()

def create_latex(data):
    os.makedirs(workspace_folder, exist_ok=True)
    
    equations = []
    
    for note in data:
        note["media_paths"] = []
        if "title_latex" in note:
            equations.append((note["guid"]+ANSWER, note["title_latex"]))
        if "solution_latex" in note:
            equations.append((note["guid"]+SOLUTION, note["solution_latex"]))
    
    media_paths = []
    
    for guid, latex in tqdm(equations):
        media_paths.append(create_latex_node(guid, latex))
    return media_paths

def create_latex_node(guid, latex):
    latex = latex.replace("%", "\\")
    svg_file = os.path.join(workspace_folder, f"{guid}.svg")

    if os.path.exists(svg_file):
        return svg_file
    
    full_latex = template.replace("<CONTENT>", latex)
    with open(tex_file, "w") as f:
        f.write(full_latex)

    p = subprocess.Popen(["dvilualatex", "-halt-on-error", f"-output-directory={workspace_folder}", tex_file],
        cwd=workspace_folder,
        stdout=subprocess.DEVNULL)
    p.wait()
    if p.returncode != 0:
        print("error", latex)
        return svg_file

    p = subprocess.Popen(["dvisvgm", dvi_file, "-e", "-c", "2,2", "-n", "-o", svg_file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)
    p.wait()
    
    return svg_file