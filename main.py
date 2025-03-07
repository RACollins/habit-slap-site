from fasthtml.common import *
from monsterui.all import *
from utils import set_theme
from config import selected_theme

### Import pages
from pages import landing, login, signup, dashboard

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

### Get theme headers and modify to include custom theme css
theme_hdrs = Theme.neutral.headers()
custom_theme_css = Link(
    rel="stylesheet", href=f"/css/{selected_theme}_theme.css", type="text/css"
)
theme_hdrs = set_theme(theme_hdrs, selected_theme)

### Bounce animation
bounce_css = Link(rel="stylesheet", href="/css/animations.css", type="text/css")

### JavaScript includes
timezone_js = Script(src="/static/js/timezone.js")
form_validation_js = Script(src="/static/js/form_validation.js")
dashboard_js = Script(src="/static/js/dashboard.js")

### Set up FastHTML app
app, rt = fast_app(
    live=True,
    pico=False,
    hdrs=(
        theme_hdrs,
        custom_theme_css,
        bounce_css,
        timezone_js,
        form_validation_js,
        dashboard_js,
    ),
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
