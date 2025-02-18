from fasthtml.common import *
from monsterui.all import *
from utils import set_theme

### Import pages
from pages import landing

### Get theme headers
theme_hdrs = Theme.neutral.headers()

## Replace the 5th header with our modified script
selected_theme = "default"
theme_hdrs = set_theme(theme_hdrs, selected_theme)

### Set up FastHTML app
app, rt = fast_app(live=True, pico=False, hdrs=theme_hdrs)

### Set up routes
landing.ar.to_app(app)

serve()
