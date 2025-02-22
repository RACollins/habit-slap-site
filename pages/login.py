from fasthtml.common import *
import fasthtml
from monsterui.all import *
from components import DaisyTopBar
import random
ar = fasthtml.APIRouter()


def MagicLinkForm(btn_text: str, target: str):
    with open("placeholder_emails.txt", "r") as file:
        placeholder_emails = file.readlines()
    placeholder_email = random.choice(placeholder_emails).strip()
    return Div(cls="hero bg-background min-h-screen")(
        Div(cls="hero-content text-center")(
            Div(cls="max-w-md")(
                H1("No Passwords. No Excuses.", cls="text-4xl font-bold"),
                P(cls="flex items-center justify-center gap-2 py-3")(
                    "Just enter your @ and click on the link."
                ),
                Form(cls="join w-full mt-4")(
                    Div(cls="relative w-full")(
                        Input(
                            type="email",
                            required=True,
                            placeholder=placeholder_email,
                            cls="input input-bordered w-full join-item validator placeholder-secondary",
                        ),
                        Div("Enter valid email address", cls="validator-hint hidden"),
                    ),
                    Button(btn_text, cls="btn btn-primary join-item"),
                    hx_post=target,
                    hx_target="#error",
                    hx_disabled_elt="#submit-btn",
                ),
            )
        )
    )


@ar.get("/login")
def get():
    return (
        Title("login"),
        DaisyTopBar(),
        MagicLinkForm("Log in", "/send_magic_link"),
    )
