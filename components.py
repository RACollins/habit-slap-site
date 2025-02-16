from fasthtml.common import *
from monsterui.all import *


def TopBar():
    return NavBar(
        A("Login", href="/login"),
        brand="Habit Slap",
    )


def theme_switcher():
    return ThemePicker()
