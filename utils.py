from fasthtml.common import *

def set_default_theme(theme_hdrs):
    ### Modify the initialization script (item #5)
    init_script = '''
        const htmlElement = document.documentElement;
        htmlElement.classList.add("dark");
        htmlElement.classList.add("uk-theme-rose");
        htmlElement.classList.add("uk-radii-md");
        htmlElement.classList.add("uk-shadows-md");
        htmlElement.classList.add("uk-font-base");
    '''
    theme_hdrs[5] = Script(init_script)
    return theme_hdrs