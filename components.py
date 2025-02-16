from fasthtml.common import *
from monsterui.all import *


def TopBar():
    return NavBar(
        A("Login", href="/login"),
        brand="Habit Slap",
        cls="px-36 py-9",
    )


def theme_switcher():
    return ThemePicker()
