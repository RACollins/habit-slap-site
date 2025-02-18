from fasthtml.common import *
from monsterui.all import *


def TopBar():
    return NavBar(
        A("Home", href="/"),
        # A("Theme", href="/theme"),
        A("Login", href="/login"),
        brand="Habit Slap",
        cls="px-36 py-9",
    )

def theme_picker():
    return ThemePicker(
        custom_themes=[
            ("Tokyo", "#869de6"),
        ],
    )