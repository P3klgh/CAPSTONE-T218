# styles_loader.py
import os

def load_stylesheets():
    stylesheet = ""
    styles_path = os.path.join(os.path.dirname(__file__), "stylesheet")

    try:
        with open(os.path.join(styles_path, "menu.qss"), "r", encoding="utf-8") as file:
            stylesheet += file.read()
            
        with open(os.path.join(styles_path, "window.qss"), "r", encoding="utf-8") as file:
            stylesheet += file.read()
    except FileNotFoundError as e:
        print(f"Error loading stylesheet: {e}")

    return stylesheet
