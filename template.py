from ast import Pass
import os

dirs = ["src", 
        os.path.join("data", "raw"),
        os.path.join("data", "pre-processed"),
        os.path.join("data", "processed"),
        "notebooks", 
        "saved_models",
    ]

for dir_ in dirs:
    os.makedirs(dir_, exist_ok=True)
    with open(os.path.join(dir_, ".gitkeep"), "w"):
        pass

files = ["dvc.yaml",
        "params.yaml",
        ".gitignore",
        os.path.join("src", "__init__.py")]

for file_ in files:
    with open(file_, "w"):
        pass
