from fasthtml.common import *
from monsterui.all import *


def DaisyTopBar():
    return Div(cls="navbar bg-base-200")(
        Div(cls="flex-1")(
            A("Habit Slap", cls="btn btn-ghost text-xl", href="/"),
        ),
        Div(cls="flex-none")(
            Ul(cls="menu menu-horizontal px-1")(
                Li(A("Login", href="/login")),
                Li(
                    Details(
                        Summary("Parent"),
                        Ul(cls="bg-base-200 rounded-t-none p-2")(
                            Li(A("Link 1")),
                            Li(A("Link 2")),
                        ),
                    )
                ),
            ),
        ),
    )


def HowItWorksCard(step):
    return Div(cls="card card-border bg-base-100 border-base-300 shadow-xl flex-1")(
        Div(cls="card-body items-center text-center")(
            H2(step["top"], cls="card-title"),
            P(step["body"], cls="text-xl my-4"),
            P(step["bottom"], cls="text-base-content"),
        )
    )


def TestimonialCard(text, author, username):
    return Div(cls="card card-border bg-base-100 border-base-300 shadow-xl")(
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
    return Div(
        cls=f"collapse collapse-arrow border border-base-300 bg-base-100 text-base-content"
    )(
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


def PricingTabs():
    return Div(cls="tabs tabs-border")(
        Input(
            type="radio",
            name="pricing_tabs",
            aria_label="7 days",
            cls="tab",
            checked="checked",
        ),
        Div(cls="tab-content border-base-300 bg-base-100 p-6")(
            "7 days",
        ),
        Input(
            type="radio",
            name="pricing_tabs",
            aria_label="1 month",
            cls="tab",
        ),
        Div(cls="tab-content border-base-300 bg-base-100 p-6")(
            "1 Month",
        ),
        Input(
            type="radio",
            name="pricing_tabs",
            aria_label="3 months",
            cls="tab",
        ),
        Div(cls="tab-content border-base-300 bg-base-100 p-6")(
            "3 Months",
        ),
        Input(
            type="radio",
            name="pricing_tabs",
            aria_label="6 months",
            cls="tab",
        ),
        Div(cls="tab-content border-base-300 bg-base-100 p-6")(
            "6 Months",
        ),
        Input(
            type="radio",
            name="pricing_tabs",
            aria_label="1 year",
            cls="tab",
        ),
        Div(cls="tab-content border-base-300 bg-base-100 p-6")(
            "1 Year",
        ),
    )
