from fasthtml.common import *
from monsterui.all import *
from utils import set_default_theme

### Import pages
from pages import landing

### Get theme headers
theme_hdrs = Theme.neutral.headers()

""" for th, theme_hdr in enumerate(theme_hdrs):
    print(th, theme_hdr)
    print("-" * 100) """

## Replace the 5th header with our modified script
theme_hdrs = set_default_theme(theme_hdrs)

### Set up FastHTML app
app, rt = fast_app(live=True, pico=False, hdrs=theme_hdrs)

### Set up routes
# theme.ar.to_app(app)
landing.ar.to_app(app)

serve()
