import os


def load_stylesheets():
    qss_files = [
        "base.qss",
        "menu.qss",
        "window.qss",
        "welcome.qss",
        "config_page.qss",
        "simulation.qss",
    ]

    stylesheet = ""
    styles_path = os.path.join(os.path.dirname(__file__), "stylesheet")

    for fname in qss_files:
        fpath = os.path.join(styles_path, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as file:
                stylesheet += file.read() + "\n"
        except FileNotFoundError:
            print(f"⚠️ Warning: {fname} not found in stylesheet folder.")

    return stylesheet
