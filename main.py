from fasthtml.common import *
from monsterui.all import *

### Import pages
from pages import landing, theme

theme_hdrs = Theme.rose.headers()

### Set up FastHTML app
app, rt = fast_app(live=True, pico=False, hdrs=theme_hdrs)


### Set up routes
theme.ar.to_app(app)
landing.ar.to_app(app)

serve()
