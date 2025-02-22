from fasthtml.common import *
from monsterui.all import *
import re
import os
from config import selected_theme


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
    return Div(cls="card bg-card shadow-xl flex-1")(
        Div(cls="card-body items-center text-center")(
            H2(step["top"], cls="card-title"),
            P(step["body"], cls="text-xl my-4"),
            P(step["bottom"], cls="text-muted-foreground"),
        )
    )


def TestimonialCard(text, author, username):
    return Div(cls="card bg-card shadow-xl")(
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


def extract_theme_colors(css_content):
    """Extract specific colors from CSS content."""
    color_vars = {
        "muted": None,
        "muted-foreground": None,
        "primary": None,
        "primary-foreground": None,
    }

    # Find all color definitions
    for line in css_content.split("\n"):
        for color_name in color_vars.keys():
            pattern = f"--{color_name}: (.*?);"
            match = re.search(pattern, line)
            if match:
                # Convert "240 13.73% 10%" to "hsl(240,13.73%,10%)"
                values = match.group(1).strip()
                color_vars[color_name] = f"[hsl({values.replace(' ', ',')})]"

    return color_vars


def load_theme_colors():
    """Load colors from all theme files."""
    theme_colors = {}
    css_dir = "css"

    for filename in os.listdir(css_dir):
        if filename.endswith("_theme.css"):
            theme_name = filename.replace("_theme.css", "")
            with open(os.path.join(css_dir, filename), "r") as f:
                css_content = f.read()
                theme_colors[theme_name] = extract_theme_colors(css_content)

    return theme_colors


### Load the colors once when the module is imported
hc_colours = load_theme_colors()


def FAQComp(question, answer):
    theme_colors = hc_colours[selected_theme]
    
    return Div(cls=f"collapse collapse-arrow bg-muted text-muted-foreground")(
        Input(type="checkbox", cls="peer"),
        Div(
            question,
            cls=f"collapse-title peer-checked:bg-{theme_colors['primary']} peer-checked:text-{theme_colors['primary-foreground']}",
        ),
        Div(
            P(answer),
            cls=f"collapse-content peer-checked:bg-{theme_colors['primary']} peer-checked:text-{theme_colors['primary-foreground']}",
        ),
    )

### Using MonsterUI Card, not DaisyUI Card
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
                cls=("btn btn-primary text-primary-foreground w-full"),
            ),
        ),
    )
