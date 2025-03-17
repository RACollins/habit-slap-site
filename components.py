from fasthtml.common import *


def DaisyTopBar():
    return Div(cls="navbar bg-base-200")(
        Div(cls="flex-1")(
            A("Habit Slap", cls="btn btn-ghost text-xl", href="/"),
        ),
        Div(cls="flex-none")(
            Ul(cls="menu menu-horizontal px-1")(
                Li(A("Login", href="/login")),
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


def PricingCardBody(plan, price, features, button_text):
    return Div(cls="card-body items-center text-center")(
        H2(plan, cls="card-title text-2xl mb-2"),
        H3(price, cls="text-secondary text-4xl font-bold mb-4"),
        Ul(cls="space-y-3 mb-6")(
            *[
                Li(cls="flex items-center gap-2")(
                    Div(
                        "✓",
                        data_tip="This is a tooltip",
                        cls="tooltip tooltip-info text-success",
                    ),
                    Span(feature),
                )
                for feature in features
            ]
        ),
        Div(cls="mt-auto w-full")(Button(button_text, cls="btn btn-primary w-full")),
    )


def PricingCard(plan, price, features, button_text):
    return Div(
        cls="card card-border bg-base-100 border-base-300 shadow-xl h-102 w-full"
    )(PricingCardBody(plan, price, features, button_text))


def PricingTabs(plans):
    container_div_style = "tab-content border-base-300 bg-base-100 p-6 w-full"
    tab_content_list = []
    for plan, plan_dict in plans.items():
        tab_content_list.append(
            Input(
                type="radio",
                name="pricing_tabs",
                aria_label=plan,
                cls="tab",
                checked="checked" if plan == "1 month" else None,
            )
        )
        tab_content_list.append(
            Div(cls=container_div_style)(
                PricingCardBody(
                    plan=plan,
                    price=plan_dict["price"],
                    features=plan_dict["features"],
                    button_text=plan_dict["button_text"],
                )
            )
        )
    return Div(cls="tabs tabs-lift")(
        *tab_content_list,
    )
