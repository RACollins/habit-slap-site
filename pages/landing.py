from fasthtml.common import *
import fasthtml
from monsterui.all import *
from components import DaisyTopBar
from lucide_fasthtml import Lucide


ar = fasthtml.APIRouter()


def MainSignUp():
    return Div(cls="hero bg-base-200 min-h-screen")(
        Div(cls="hero-content text-center")(
            Div(cls="max-w-md")(
                H1("Habit Slap", cls="text-5xl font-bold"),
                P(cls="flex items-center justify-center gap-2 py-3")(
                    "Motivation like a slap in the face",
                    Lucide("hand", cls="text-primary"),
                    Lucide("sparkles", cls="text-primary"),
                ),
                Button("Get Started", cls="btn btn-primary py-3"),
                P("Scroll down to learn more", cls="text-accent py-3"),
                A("↓", href="#how-it-works", cls="text-2xl bounce-animation"),
            ),
        ),
    )


@ar.get("/")
def get():
    return Title("Habit Slap"), DaisyTopBar(), MainSignUp()
