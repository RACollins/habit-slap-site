from fasthtml.common import *
import fasthtml
from monsterui.all import *
from components import TopBar, theme_switcher

ar = fasthtml.APIRouter()

def MainSignUp():
    return Container(
        Article(
            ArticleTitle("Habit Slap"),
            Subtitle(
                "Motivation like a slap in the face ✋💥"
            ),
            A(Button("Get Started", type="button"), href="/login"),
            P("Scroll down to learn more", cls="text-blue-500"),
            A("↓", href="#how-it-works"),
            cls="main-signup",
        ),
    )

@ar.get("/")
def get():
    return Title("Habit Slap"), TopBar(), MainSignUp()

