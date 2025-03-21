from fasthtml.common import *
import fasthtml
from components import DaisyTopBar
import random
import os
import yagmail
import secrets
from dotenv import load_dotenv
from database.dynamo_handler import DynamoHandler
from datetime import datetime, timedelta, timezone

load_dotenv()
db = DynamoHandler()
is_dev = os.getenv("IS_DEV")
site_url = "http://0.0.0.0:5001" if is_dev else "https://habit-slap.vercel.app"
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ar = fasthtml.APIRouter()


def MagicLinkForm(btn_text: str, target: str):

    with open(os.path.join(root_dir, "placeholders/emails.txt"), "r") as file:
        placeholder_emails = file.readlines()
    placeholder_email = random.choice(placeholder_emails).strip()

    return Div(cls="hero bg-background min-h-screen")(
        Div(cls="hero-content text-center")(
            Div(cls="max-w-md")(
                H1("No Passwords. No Excuses.", cls="text-3xl font-bold"),
                P(cls="flex items-center justify-center gap-2 py-3")(
                    "Just enter your @ and click on the link."
                ),
                Form(cls="join w-full mt-4")(
                    Div(cls="relative w-full")(
                        Input(
                            type="email",
                            name="email",
                            required=True,
                            placeholder=placeholder_email,
                            cls="input input-bordered bg-base-100 w-full join-item validator placeholder-slate-500",
                            pattern=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
                            data_validation="Please enter a valid email address",
                            data_validation_type="email",
                        ),
                        Div("Enter valid email address", cls="validator-hint hidden"),
                    ),
                    Button(btn_text, cls="btn btn-primary join-item", id="submit-btn"),
                    hx_post=target,
                    hx_target="#error",
                    hx_disabled_elt="#submit-btn",
                ),
                Div(id="error", cls="mt-4"),
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


def send_magic_link_email(email: str, magic_link: str):
    # Get credentials from environment variables
    sender_email = os.getenv("GMAIL_USER")
    sender_password = os.getenv("GMAIL_PASSWORD")

    if not sender_email or not sender_password:
        raise Exception("Email credentials not configured")

    email_content = f"""
    Hi there,
  
    Click this link to sign in to Habit Slap: {magic_link}
  
    If you didn't request this, just ignore this email.
  
    Cheers,
    The Habit Slap Team
    """

    # Initialize yagmail SMTP client
    yag = yagmail.SMTP(sender_email, sender_password)

    try:
        # Send email
        yag.send(to=email, subject="Sign in to Habit Slap", contents=email_content)
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        raise e
    finally:
        yag.close()


@ar.post("/send_magic_link")
def post(email: str):
    # Validate email
    if not email:
        return Div("Email is required", cls="text-error text-center", id="error")

    try:
        # Get or create user
        is_new_user = False
        user = db.get_user(email)
        if not user:
            is_new_user = True
            user = {
                "email": email,
                "is_active": False,
                "magic_link_token": None,
                "magic_link_expiry": None,
                "tier": "free",  # Add default tier when creating user
            }
            db.create_user(user)

        # Generate magic link
        magic_link_token = secrets.token_urlsafe(32)
        magic_link_expiry = datetime.now(timezone.utc) + timedelta(minutes=15)

        # Update user with magic link info
        db.update_user(
            email,
            {
                "magic_link_token": magic_link_token,
                "magic_link_expiry": magic_link_expiry.isoformat(),
            },
        )

        try:
            # Send email
            magic_link = f"{site_url}/verify_magic_link/{magic_link_token}"
            send_magic_link_email(email, magic_link)
        except Exception as email_error:
            # Clean up based on user status
            if is_new_user:
                # Delete the newly created user
                db.delete_user(email)
            else:
                # Reset magic link info for existing user
                db.update_user(
                    email,
                    {
                        "magic_link_token": None,
                        "magic_link_expiry": None,
                    },
                )
            raise email_error

        # Return success response
        return (
            Div(
                P(
                    "Check your inbox. Link will expire in 15 minutes.",
                    cls="text-success text-center",
                ),
                id="error",
            ),
            HttpHeader("HX-Reswap", "innerHTML"),
            Button(
                "Magic link sent",
                type="submit",
                id="submit-btn",
                disabled=True,
                cls="btn btn-primary join-item",
                hx_swap_oob="true",
            ),
        )
    except Exception as e:
        # Return error response
        return Div(
            f"Failed to send magic link: {str(e)}",
            cls="text-error text-center",
            id="error",
        )


@ar.get("/verify_magic_link/{token}")
def get(session, token: str):
    now = datetime.now(timezone.utc)
    user = db.query_by_token(token)

    if user and datetime.fromisoformat(user["magic_link_expiry"]) > now:
        session["auth"] = user["email"]
        db.update_user(
            user["email"],
            {"magic_link_token": None, "magic_link_expiry": None, "is_active": True},
        )
        # Check if user has already signed up by looking for the name field
        if not user.get("name"):
            return RedirectResponse("/signup")
        return RedirectResponse("/dashboard")
    return "Invalid or expired magic link"
