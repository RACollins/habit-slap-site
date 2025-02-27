from fasthtml.common import *
import json
import datetime
import pytz


def set_theme(theme_hdrs: list[Script], selected_theme: str) -> list[Script]:
    """Sets the theme for the application by modifying header scripts.

    Loads theme options and site themes from JSON files, validates the selected theme
    against available options, and generates a JavaScript initialization script to
    apply the theme classes to the document root element.

    Args:
        theme_hdrs (list): List of header elements, where index 5 contains the theme script
        selected_theme (str): Name of the theme to apply from site_themes.json

    Returns:
        list: Modified theme_hdrs with updated initialization script at index 5
    """
    ### Get default options and site themes JSONs
    with open("themes/theme_options.json", "r") as f:
        theme_options = json.load(f)
    with open("themes/site_themes.json", "r") as f:
        site_themes = json.load(f)

    ### Get the selected theme
    selected_theme_dict = site_themes[selected_theme]

    ### check value exists in theme_options, return default if not
    checked_theme = {
        option: value if value in theme_options[option] else theme_options[option][0]
        for option, value in selected_theme_dict.items()
    }

    ### Modify the initialization script (item #5)
    init_script = f"""
        const htmlElement = document.documentElement;
        htmlElement.classList.add("uk-theme-{checked_theme["color"]}");
        htmlElement.classList.add("uk-radii-{checked_theme["radii"]}");
        htmlElement.classList.add("uk-shadows-{checked_theme["shadows"]}");
        htmlElement.classList.add("uk-font-{checked_theme["font"]}");
        htmlElement.classList.add("{checked_theme["mode"]}");
    """
    theme_hdrs[5] = Script(init_script)
    return theme_hdrs


def convert_local_to_utc(date_str, time_str, timezone):
    """
    Convert a local date and time to UTC ISO format

    Args:
        date_str: Date in format YYYY-MM-DD
        time_str: Time in format HH:MM
        timezone: Timezone string (e.g., 'America/New_York')

    Returns:
        UTC datetime in ISO format with timezone info (e.g., '2025-01-29T08:25:00+00:00')
    """
    if not timezone:
        timezone = "UTC"  # Default to UTC if no timezone provided

    # Parse the date and time strings
    local_datetime_str = f"{date_str} {time_str}"
    local_datetime = datetime.datetime.strptime(local_datetime_str, "%Y-%m-%d %H:%M")

    # Get the timezone object
    tz = pytz.timezone(timezone)

    # Localize the datetime to make it timezone-aware
    local_datetime = tz.localize(local_datetime)

    # Convert to UTC
    utc_datetime = local_datetime.astimezone(pytz.UTC)

    # Return in ISO format
    return utc_datetime.isoformat()
