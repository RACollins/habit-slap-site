from fasthtml.common import *
import fasthtml
from monsterui.all import *
from components import DaisyTopBar, HowItWorksCard
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
                A("↓", href="#how-it-works", cls="text-2xl bounce-animation scroll-smooth"),
            ),
        ),
    )


def HowItWorks():
    card_content = {
        "step1": {
            "top": "Step 1",
            "body": "🎯 Set a Goal",
            "bottom": "Sign up with your email and set a goal.",
        },
        "step2": {
            "top": "Step 2",
            "body": "💪 Get Motivated",
            "bottom": "Recieve daily emails with motivational messages tailored to you.",
        },
        "step3": {
            "top": "Step 3",
            "body": "🏅 Get Sh*t Done!",
            "bottom": "No more excuses! Build that habit! Attack your week! Also works well for quitting bad habits.",
        },
    }
    return Div(cls="container mx-auto py-16")(
        H2("How it Works", cls="text-4xl font-bold text-center mb-12"),
        Div(
            *[HowItWorksCard(card_content[f"step{i+1}"]) for i in range(3)],
            cls="flex flex-col md:flex-row gap-8 justify-center items-stretch px-4",
        ),
        id="how-it-works",
    )


@ar.get("/")
def get():
    return (
        Title("Habit Slap"),
        Style("html { scroll-behavior: smooth; }"),
        DaisyTopBar(),
        MainSignUp(),
        HowItWorks()
    )
