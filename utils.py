from fasthtml.common import *
import json
import datetime
import pytz
import os
import re


def convert_local_to_utc(time_str, timezone):
    """
    Convert a local time to UTC time string

    Args:
        time_str: Time in format HH:MM
        timezone: Timezone string (e.g., 'America/New_York')

    Returns:
        UTC time string in HH:MM format
    """
    if not timezone:
        timezone = "UTC"  # Default to UTC if no timezone provided

    # Parse the time string
    time_parts = datetime.datetime.strptime(time_str, "%H:%M")

    # Create a timezone-aware datetime for today with the given time
    tz = pytz.timezone(timezone)
    local_today = datetime.datetime.now(tz).replace(
        hour=time_parts.hour, minute=time_parts.minute, second=0, microsecond=0
    )

    # Convert to UTC
    utc_time = local_today.astimezone(pytz.UTC)

    # Return only the time part in HH:MM format
    return utc_time.strftime("%H:%M")


def remove_existing_theme(output_path, theme_name):
    """
    Removes an existing theme from the output.css file.

    This is useful when a theme is partially included or corrupted and needs to be replaced.

    Args:
        output_path (str): Path to the output.css file
        theme_name (str): Name of the theme to remove

    Returns:
        bool: True if theme was found and removed, False otherwise
    """
    try:
        with open(output_path, "r") as file:
            content = file.read()

        # Look for the theme section
        theme_pattern = re.compile(
            r"@layer\s+base\s+\{\s*:root:has\(input\.theme-controller\[value="
            + re.escape(theme_name)
            + r"\]:checked\),\[data-theme="
            + re.escape(theme_name)
            + r"\].*?\}",
            re.DOTALL,
        )

        # Check if the theme exists
        if not theme_pattern.search(content):
            return False

        # Remove the theme section
        new_content = theme_pattern.sub("", content)

        # Write the modified content back
        with open(output_path, "w") as file:
            file.write(new_content)

        return True
    except Exception as e:
        print(f"Error removing existing theme: {e}")
        return False


def append_themes(force=False, replace=False):
    """
    Appends themes.css to output.css if not already included.

    This function checks if the themes are already in the output.css file
    to avoid duplicate appending. It uses a more robust pattern matching
    approach to detect if the theme content is already present.

    Args:
        force (bool): If True, append the themes even if they appear to be already present
        replace (bool): If True, remove any existing theme before appending

    Returns:
        None
    """
    themes_path = "static/css/themes.css"
    output_path = "static/css/output.css"

    if not os.path.exists(themes_path):
        print(f"Error: Could not find {themes_path}")
        return

    if not os.path.exists(output_path):
        print(f"Error: Could not find {output_path}")
        return

    # Read themes content
    with open(themes_path, "r") as themes_file:
        themes_content = themes_file.read().strip()

    # Extract the theme name for potential removal
    theme_name_match = re.search(
        r":root:has\(input\.theme-controller\[value=(\w+)\]:checked\)", themes_content
    )
    theme_name = (
        theme_name_match.group(1) if theme_name_match else "mytheme"
    )  # Default to mytheme if not found

    # If replace is True, remove any existing theme
    if replace:
        print(f"Attempting to remove existing '{theme_name}' theme...")
        if remove_existing_theme(output_path, theme_name):
            print(f"Existing '{theme_name}' theme removed successfully.")
        else:
            print(f"No existing '{theme_name}' theme found to remove.")
        # Force append after removal
        force = True

    # If force is True, skip the check and append anyway
    if not force:
        # Read output content
        with open(output_path, "r") as output_file:
            output_content = output_file.read()

        # Extract the theme selector pattern from themes.css
        # This looks for the main theme selector which should be unique to the theme
        theme_selector_match = re.search(
            r"(:root:has\(input\.theme-controller\[value=(\w+)\]:checked\),\[data-theme=(\w+)\])",
            themes_content,
        )

        if theme_selector_match:
            theme_selector = theme_selector_match.group(1)
            theme_name = theme_selector_match.group(2)  # Extract the theme name

            # Check if this specific theme selector exists in the output file
            if theme_selector in output_content:
                # Now extract a few CSS properties from the themes.css file to use as verification
                # This is more flexible than hard-coding values
                css_properties = re.findall(r"--color-[\w-]+:\s*[^;]+", themes_content)

                # Take a sample of properties (first, middle, and last) if enough exist
                sample_size = min(3, len(css_properties))
                if sample_size > 0:
                    sample_properties = [css_properties[0]]
                    if sample_size > 1:
                        sample_properties.append(
                            css_properties[len(css_properties) // 2]
                        )
                    if sample_size > 2:
                        sample_properties.append(css_properties[-1])

                    # Check if all sampled properties exist in the output file
                    if all(prop in output_content for prop in sample_properties):
                        print(
                            f"Theme '{theme_name}' from {themes_path} is already in {output_path}. Skipping append."
                        )
                        return
                    else:
                        print(
                            f"Theme selector found but properties don't match. Will append the theme."
                        )
                else:
                    print(
                        f"No CSS properties found in {themes_path}. Will append the theme."
                    )
            else:
                print(
                    f"Theme selector not found in {output_path}. Will append the theme."
                )
        else:
            print(
                f"Could not identify theme selector in {themes_path}. Will append the theme."
            )
    else:
        print(f"Force mode enabled. Appending themes regardless of current content.")

    # If we get here, the theme is not in the output file or force is True
    print(f"Adding themes from {themes_path} to {output_path}...")

    # Append themes to output
    with open(output_path, "a") as output_file:
        # Add a newline to ensure clean separation
        output_file.write("\n")
        output_file.write(themes_content)

    print(f"Successfully appended {themes_path} to {output_path}")
