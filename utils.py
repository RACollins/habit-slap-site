from fasthtml.common import *
import datetime
import pytz


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