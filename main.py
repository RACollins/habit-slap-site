from fasthtml.common import *
from monsterui.all import *
from components import TopBar, theme_switcher

### Import pages
import pages.landing

theme_hdrs = Theme.rose.headers()

### Set up FastHTML app
app, rt = fast_app(live=True, pico=False, hdrs=theme_hdrs)


### Set up routes
pages.landing.ar.to_app(app)

serve()
