import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR)) # 2 folders up


# Constants here

SCORE_PATH = "/local/score.txt"
LEVEL_PATH = "/local/level.txt"
FONT_PATH = ROOT_DIR + "/assets/Tiny5.ttf"

# Constants here


def read_txt(path):
    file_path = f"{ROOT_DIR}{path}"
    # print("paths.py read_txt", file_path)
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        print(f"Read file {path}")

        return content



"""Deletes everything inside the file and writes new "content"!! """
def write_txt(path, content):
    file_path = f"{ROOT_DIR}{path}"
    # print("paths.py read_txt", file_path)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(str(content))