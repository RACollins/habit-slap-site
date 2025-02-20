from fasthtml.common import *
from monsterui.all import *


def TopBar():
    return NavBar(
        A("Home", href="/"),
        # A("Theme", href="/theme"),
        A("Login", href="/login"),
        brand="Habit Slap",
    )


def DaisyTopBar():
    return Div(
        Div(
            A("Habit Slap", cls="btn btn-ghost text-xl", href="/"),
            cls="flex-1",
        ),
        Div(
            Ul(
                Li(A("Login", href="/login")),
                Li(
                    Details(
                        Summary("Parent"),
                        Ul(
                            Li(A("Link 1")),
                            Li(A("Link 2")),
                            cls="bg-base-100 rounded-t-none p-2",
                        ),
                    )
                ),
                cls="menu menu-horizontal px-1",
            ),
            cls="flex-none",
        ),
        cls="navbar bg-base-100",
    )


def theme_picker():
    return ThemePicker(
        custom_themes=[
            ("Tokyo", "#869de6"),
        ],
    )


def HowItWorksCard(step):
    return Div(cls="card bg-muted shadow-xl flex-1")(
        Div(cls="card-body items-center text-center")(
            H2(step["top"], cls="card-title"),
            P(step["body"], cls="text-xl my-4"),
            P(step["bottom"], cls="text-muted-foreground"),
        )
    )

def TestimonialCard(text, author, username):
    return Div(cls="card bg-muted shadow-xl")(
        Div(cls="card-body")(
            # Large quotation mark
            Div('"', cls="text-4xl text-primary mb-4"),
            # Testimonial text
            P(text, cls="text-lg mb-4"),
            # Author info
            Div(cls="mt-auto")(
                H3(author, cls="font-bold"),
                P(f"@{username}", cls="text-sm text-base-content/60"),
            )
        )
    )
