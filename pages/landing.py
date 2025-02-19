from fasthtml.common import *
import fasthtml
from monsterui.all import *
from components import DaisyTopBar

ar = fasthtml.APIRouter()


def MainSignUp():
    return Div(cls="hero bg-base-200 min-h-screen")(
        Div(cls="hero-content text-center")(
            Div(cls="max-w-md")(
                H1("Habit Slap", cls="text-5xl font-bold"),
                P(
                    "Motivation like a slap in the face ✋💥",
                    cls="py-6",
                ),
                Button("Get Started", cls="btn btn-primary"),
                P("Scroll down to learn more", cls="text-accent py-3"),
                A("↓", href="#how-it-works"),
            ),
        ),
    )


@ar.get("/")
def get():
    return Title("Habit Slap"), DaisyTopBar(), MainSignUp()
