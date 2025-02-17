from fasthtml.common import *
import fasthtml
from monsterui.all import *
from components import TopBar

ar = fasthtml.APIRouter()


def theme_switcher():
    return ThemePicker()


@ar.get("/theme")
def get():
    return Title("Theme"), TopBar(), theme_switcher()
