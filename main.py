from fasthtml.common import *
from monsterui.all import *
from utils import set_theme

### Import pages
from pages import landing

### Get theme headers and modify to include custom theme css
selected_theme = "black-ruby"
theme_hdrs = Theme.neutral.headers()
custom_theme_css = Link(
    rel="stylesheet", href=f"/css/{selected_theme}_theme.css", type="text/css"
)
theme_hdrs = set_theme(theme_hdrs, selected_theme)

### Set up FastHTML app
app, rt = fast_app(live=True, pico=False, hdrs=(theme_hdrs, custom_theme_css))

### Set up routes
landing.ar.to_app(app)

serve()
