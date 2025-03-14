from fasthtml.common import *
from monsterui.all import *


def DaisyTopBar():
    return Div(cls="navbar bg-base-300")(
        Div(cls="flex-1")(
            A("Habit Slap", cls="btn btn-ghost text-xl", href="/"),
        ),
        Div(cls="flex-none")(
            Ul(cls="menu menu-horizontal px-1")(
                Li(A("Login", href="/login")),
                Li(
                    Details(
                        Summary("Parent"),
                        Ul(cls="bg-base-300 rounded-t-none p-2")(
                            Li(A("Link 1")),
                            Li(A("Link 2")),
                        ),
                    )
                ),
            ),
        ),
    )


def HowItWorksCard(step):
    return Div(cls="card bg-base-200 shadow-xl flex-1")(
        Div(cls="card-body items-center text-center")(
            H2(step["top"], cls="card-title"),
            P(step["body"], cls="text-xl my-4"),
            P(step["bottom"], cls="text-base-content"),
        )
    )


def TestimonialCard(text, author, username):
    return Div(cls="card bg-base-200 shadow-xl")(
        Div(cls="card-body")(
            # Large quotation mark
            Div('"', cls="text-4xl text-primary mb-4"),
            # Testimonial text
            P(text, cls="text-lg text-base-content mb-4"),
            # Author info
            Div(cls="mt-auto")(
                H3(author, cls="font-bold"),
                P(f"@{username}", cls="text-sm text-base-content"),
            ),
        )
    )


def FAQComp(question, answer):
    return Div(cls=f"collapse collapse-arrow bg-base-200 text-base-content")(
        Input(type="checkbox", cls="peer"),
        Div(
            question,
            cls=f"collapse-title peer-checked:bg-primary peer-checked:text-primary-content",
        ),
        Div(
            P(answer),
            cls=f"collapse-content peer-checked:bg-primary peer-checked:text-primary-content",
        ),
    )


### Using MonsterUI Card, not DaisyUI Card
def PricingCard(plan, price, features):
    return Card(
        Div(cls="p-12")(  # Added padding container
            DivVStacked(
                cls="space-y-1"
            )(  # Center and vertically stack the plan name and price
                H2(plan),
                H3(price, cls="text-primary"),
                P("per month"),
            ),
            # DivHStacked makes green check and feature Li show up on same row instead of newline
            Ul(cls="space-y-4 my-6")(  # Added vertical margin
                *[
                    DivHStacked(UkIcon("check", cls="text-green-500 mr-2"), Li(feature))
                    for feature in features
                ],
            ),
            Button(
                "Subscribe Now",
                cls=("btn btn-primary text-primary-foreground w-full"),
            ),
        ),
    )
