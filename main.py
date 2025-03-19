from fasthtml.common import *
import argparse
import subprocess

### Import pages
from pages import landing, login, signup, dashboard

### Bring in command line arguments
parser = argparse.ArgumentParser(
    prog="FastHTML with Tailwind CSS and DaisyUI",
    description="FastHTML app using Tailwind CSS for styling",
)
parser.add_argument(
    "-rt",
    "--reload_tailwind",
    action="store_true",
    help="Run the Tailwind CLI build",
)

args = parser.parse_args()

### Reload Tailwind CSS, dev only
if args.reload_tailwind:
    print("Running Tailwind CSS build...")
    subprocess.run(
        ["./tailwindcss", "-i", "static/css/input.css", "-o", "static/css/output.css"]
    )

### Set up beforeware
login_redir = RedirectResponse("/login", status_code=303)


def before(req, session):
    auth = req.scope["auth"] = session.get("auth", None)
    # Only redirect to login for protected routes
    if not auth and req.url.path == "/dashboard":
        return login_redir


bware = Beforeware(
    before,
    skip=[
        "/",
        r"/favicon\.ico",
        r"/static/.*",
        r".*\.css",
        "/login",
        "/send_magic_link",
        r"/verify_magic_link/.*",
        "/signup",
        "/complete_signup",
    ],
)

### Bounce animation
bounce_css = Link(rel="stylesheet", href="/static/css/animations.css", type="text/css")

### Tailwind CSS with DaisyUI
tailwind_css = Link(rel="stylesheet", href="/static/css/output.css", type="text/css")

### Theme CSS
theme_css = Link(rel="stylesheet", href="/static/css/themes.css", type="text/css")

### JavaScript includes
timezone_js = Script(src="/static/js/timezone.js")
form_validation_js = Script(src="/static/js/form_validation.js")
dashboard_js = Script(src="/static/js/dashboard.js")

### Set up FastHTML app (force background colour)
app, rt = fast_app(
    live=True,
    pico=False,
    hdrs=(
        bounce_css,
        tailwind_css,
        theme_css,
        Style("body { background-color: var(--color-base-200) !important; }"),
        timezone_js,
        form_validation_js,
        dashboard_js,
    ),
    htmlkw=dict(lang="en", dir="ltr", data_theme="grey_ruby"),
)


### Set up routes
landing.ar.to_app(app)
login.ar.to_app(app)
signup.ar.to_app(app)
dashboard.ar.to_app(app)


@rt("/set_timezone")
def post(session, timezone: str):
    session["timezone"] = timezone
    return "OK"


serve()
