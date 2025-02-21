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
            P(text, cls="text-lg text-foreground mb-4"),
            # Author info
            Div(cls="mt-auto")(
                H3(author, cls="font-bold"),
                P(f"@{username}", cls="text-sm text-muted-foreground"),
            ),
        )
    )


def FAQComp(question, answer):
    # Had to hard code the colors because the semanitc names were not working
    # May revisit in the future
    hc_colours = {
        "bg-muted": "bg-[hsl(214,12%,15%)]",
        "text-muted-foreground": "text-[hsl(214,12%,65%)]",
        "bg-primary": "bg-[hsl(346,62%,48%)]",
        "text-primary-foreground": "text-[hsl(0,0%,100%)]",
    }
    return Div(
        cls=f"collapse collapse-arrow bg-muted text-muted-foreground"
    )(
        Input(type="checkbox", cls="peer"),
        Div(
            question,
            cls=f"collapse-title peer-checked:{hc_colours['bg-primary']} peer-checked:{hc_colours['text-primary-foreground']}",
        ),
        Div(
            P(answer),
            cls=f"collapse-content peer-checked:{hc_colours['bg-primary']} peer-checked:{hc_colours['text-primary-foreground']}",
        ),
    )


def PricingCard(plan, price, features):
    return Card(
        Div(cls="p-12")(  # Added padding container
            DivVStacked(  # Center and vertically stack the plan name and price
                H2(plan),
                H3(price, cls="text-primary"),
                P("per month"),
                cls="space-y-1",
            ),
            # DivHStacked makes green check and feature Li show up on same row instead of newline
            Ul(
                *[
                    DivHStacked(UkIcon("check", cls="text-green-500 mr-2"), Li(feature))
                    for feature in features
                ],
                cls="space-y-4 my-6",  # Added vertical margin
            ),
            Button(
                "Subscribe Now",
                cls=("button bg-primary text-primary-foreground", "w-full"),
            ),
        ),
    )
