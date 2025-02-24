from fasthtml.common import *
import json


def set_theme(theme_hdrs: list[Script], selected_theme: str) -> list[Script]:
    """Sets the theme for the application by modifying header scripts.

    Loads theme options and site themes from JSON files, validates the selected theme
    against available options, and generates a JavaScript initialization script to
    apply the theme classes to the document root element.

    Args:
        theme_hdrs (list): List of header elements, where index 5 contains the theme script
        selected_theme (str): Name of the theme to apply from site_themes.json

    Returns:
        list: Modified theme_hdrs with updated initialization script at index 5
    """
    ### Get default options and site themes JSONs
    with open("themes/theme_options.json", "r") as f:
        theme_options = json.load(f)
    with open("themes/site_themes.json", "r") as f:
        site_themes = json.load(f)

    ### Get the selected theme
    selected_theme_dict = site_themes[selected_theme]

    ### check value exists in theme_options, return default if not
    checked_theme = {
        option: value if value in theme_options[option] else theme_options[option][0]
        for option, value in selected_theme_dict.items()
    }

    ### Modify the initialization script (item #5)
    init_script = f"""
        const htmlElement = document.documentElement;
        htmlElement.classList.add("uk-theme-{checked_theme["color"]}");
        htmlElement.classList.add("uk-radii-{checked_theme["radii"]}");
        htmlElement.classList.add("uk-shadows-{checked_theme["shadows"]}");
        htmlElement.classList.add("uk-font-{checked_theme["font"]}");
        htmlElement.classList.add("{checked_theme["mode"]}");
    """
    theme_hdrs[5] = Script(init_script)
    return theme_hdrs
