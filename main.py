from fasthtml.common import *
from monsterui.all import *
from utils import set_theme
from config import selected_theme

### Import pages
from pages import landing, login

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

### Set up FastHTML app
app, rt = fast_app(live=True, pico=False, hdrs=(theme_hdrs, custom_theme_css))

### Set up routes
landing.ar.to_app(app)
login.ar.to_app(app)

serve()
