from fasthtml.common import *
from monsterui.all import *
from components import TopBar, theme_switcher


theme_hdrs = Theme.rose.headers()

### Set up FastHTML app
app, rt = fast_app(live=True, pico=False, hdrs=theme_hdrs)


### Set up routes
@rt("/")
def get():
    return Title("Habit Slap"), TopBar(), theme_switcher()


serve()
