from fasthtml.common import *
import fasthtml

# from monsterui.all import *
from lucide_fasthtml import Lucide
from database.dynamo_handler import DynamoHandler
import datetime
from utils import convert_local_to_utc

ar = fasthtml.APIRouter()

### Initialize database
db = DynamoHandler()


def SidebarContent():
    return Div(cls="h-full")(
        Div(cls="text-xl font-bold p-4 border-b")("Habit Slap"),
        Ul(cls="menu p-4 w-80 min-h-full bg-card text-card-foreground")(
            Li()(
                A(
                    cls="sidebar-link",
                    href="#personal",
                    data_target="personal-content",
                )(Div(cls="flex items-center")(Lucide("user", cls="mr-2"), "Personal"))
            ),
            Li()(
                A(
                    cls="sidebar-link",
                    href="#habit",
                    data_target="habit-content",
                )(
                    Div(cls="flex items-center")(
                        Lucide("pencil-line", cls="mr-2"), "Habit"
                    )
                )
            ),
            Li()(
                A(
                    cls="sidebar-link",
                    href="#preferences",
                    data_target="preferences-content",
                )(
                    Div(cls="flex items-center")(
                        Lucide("settings", cls="mr-2"), "Preferences"
                    )
                )
            ),
            Div(cls="divider my-2"),
            Li()(
                A(
                    href="/signout",
                    hx_post="/signout",
                    hx_confirm="Are you sure you want to sign out?",
                )(
                    Div(cls="flex items-center")(
                        Lucide("log-out", cls="mr-2"), "Sign out"
                    )
                )
            ),
            Li()(
                # Collapse component for delete account
                Div(cls="collapse bg-card")(
                    Input(type="checkbox", cls="peer"),
                    Div(
                        cls="collapse-title p-0",  # Remove default padding
                    )(
                        A(
                            cls="flex items-center text-error",
                            href="#",  # Prevent navigation but keep styling
                        )(Lucide("trash-2", cls="mr-2"), "Delete Account")
                    ),
                    Div(cls="collapse-content")(
                        P(
                            cls="text-sm text-warning mb-4",
                        )("Warning: This action cannot be undone."),
                        Button(
                            type="button",
                            cls="btn btn-error btn-sm w-full",
                            onclick="delete_account_modal.showModal()",
                        )("Delete My Account"),
                        # Modal for final confirmation
                        Dialog(
                            cls="modal",
                            id="delete_account_modal",
                        )(
                            Div(cls="modal-box")(
                                H3(cls="font-bold text-lg")("Confirm Account Deletion"),
                                P(cls="py-4")(
                                    "Are you sure you want to delete your account? This action cannot be undone."
                                ),
                                Div(cls="modal-action")(
                                    Button(
                                        "Cancel",
                                        cls="btn",
                                        onclick="delete_account_modal.close()",
                                    ),
                                    Button(
                                        "Delete",
                                        cls="btn btn-error",
                                        hx_post="/delete_account",
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )


def PreferencesContent(user):
    """Generate the preferences section content"""
    # Get user preferences with default values if not set
    delivery_time = user.get("delivery_time_original", "09:00")
    time_period = user.get("time_period_original", "AM")
    formality = user.get("formality", "50")
    assertiveness = user.get("assertiveness", "50")
    intensity = user.get("intensity", "50")

    return Div(cls="hero-content")(
        Div(cls="card w-full bg-card text-card-foreground shadow-xl")(
            Div(cls="card-body")(
                Form(
                    action="/dashboard/update",
                    method="post",
                    id="preferences-form",
                )(
                    Fieldset(
                        cls="fieldset bg-background border border-accent p-4 rounded-box"
                    )(
                        Legend("Email Preferences", cls="fieldset-legend"),
                        # Delivery Time
                        Label("Delivery Time", cls="fieldset-label"),
                        Div(cls="join w-full")(
                            Input(
                                type="time",
                                id="delivery_time",
                                name="delivery_time",
                                value=delivery_time,
                                cls="input input-bordered join-item w-full",
                            ),
                            Select(
                                Option(
                                    "AM", value="AM", selected=(time_period == "AM")
                                ),
                                Option(
                                    "PM", value="PM", selected=(time_period == "PM")
                                ),
                                id="time_period",
                                name="time_period",
                                cls="select select-bordered join-item",
                            ),
                        ),
                        P(cls="text-sm opacity-70 mb-4")(
                            "When would you like to receive your daily motivation?",
                        ),
                        # Email Style
                        Label("Email Style", cls="fieldset-label mt-4"),
                        # Formality Slider
                        Label("Formality", cls="fieldset-label"),
                        Div(cls="w-full")(
                            Input(
                                type="range",
                                min="0",
                                max="100",
                                value=formality,
                                cls="range range-primary",
                                id="formality",
                                name="formality",
                            ),
                            Div(cls="flex justify-between px-2 text-xs mb-4")(
                                Span("Casual & Friendly"), Span("Formal & Professional")
                            ),
                        ),
                        # Assertiveness Slider
                        Label("Assertiveness", cls="fieldset-label"),
                        Div(cls="w-full")(
                            Input(
                                type="range",
                                min="0",
                                max="100",
                                value=assertiveness,
                                cls="range range-secondary",
                                id="assertiveness",
                                name="assertiveness",
                            ),
                            Div(cls="flex justify-between px-2 text-xs mb-4")(
                                Span("Gentle & Supportive"),
                                Span("Direct & Challenging"),
                            ),
                        ),
                        # Intensity Slider
                        Label("Emotional Intensity", cls="fieldset-label"),
                        Div(cls="w-full")(
                            Input(
                                type="range",
                                min="0",
                                max="100",
                                value=intensity,
                                cls="range range-accent",
                                id="intensity",
                                name="intensity",
                            ),
                            Div(cls="flex justify-between px-2 text-xs")(
                                Span("Calm & Measured"), Span("Passionate & Energetic")
                            ),
                        ),
                        P(cls="text-sm opacity-70 mt-1")(
                            "Adjust these sliders to customize the tone and style of your motivational emails.",
                        ),
                        # Save Button
                        Div(cls="mt-6 text-right")(
                            Button(
                                "Save Changes",
                                type="submit",
                                cls="btn btn-primary",
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )


def PersonalContent(user):
    """Generate the personal section content"""
    # Get user data with default values if not set
    name = user.get("name", "")
    bio = user.get("bio", "")

    return Div(cls="hero-content")(
        Div(cls="card w-full bg-card shadow-xl")(
            Div(cls="card-body")(
                Form(
                    action="/dashboard/update",
                    method="post",
                    id="personal-form",
                )(
                    Fieldset(
                        cls="fieldset bg-background border border-accent p-4 rounded-box"
                    )(
                        Legend("Personal Information", cls="fieldset-legend"),
                        # Name
                        Label("Name", cls="fieldset-label"),
                        Input(
                            type="text",
                            id="name",
                            name="name",
                            value=name,
                            cls="input input-bordered w-full",
                            placeholder="John Doe",
                        ),
                        # Bio
                        Label("Bio", cls="fieldset-label mt-4"),
                        Textarea(
                            bio,
                            id="bio",
                            name="bio",
                            cls="textarea textarea-bordered w-full h-24",
                            placeholder="Tell us a little bit about yourself",
                        ),
                        # Save Button
                        Div(cls="mt-6 text-right")(
                            Button(
                                "Save Changes",
                                type="submit",
                                cls="btn btn-primary",
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )


def HabitContent(user):
    """Generate the habit section content"""
    # Get user data with default values if not set
    habit_details = user.get("habit_details", "")
    timeframe = user.get("timeframe", "")

    return Div(cls="hero-content")(
        Div(cls="card w-full bg-card shadow-xl")(
            Div(cls="card-body")(
                Form(
                    action="/dashboard/update",
                    method="post",
                    id="habit-form",
                )(
                    Fieldset(
                        cls="fieldset bg-background border border-accent p-4 rounded-box"
                    )(
                        Legend("Habit Information", cls="fieldset-legend"),
                        # Habit Details
                        Label("What do you want to achieve?", cls="fieldset-label"),
                        Textarea(
                            habit_details,
                            id="habit_details",
                            name="habit_details",
                            cls="textarea textarea-bordered w-full h-32",
                            placeholder="Be honest, realistic, and precise.",
                        ),
                        # Time Frame
                        Label("Time Frame", cls="fieldset-label mt-4"),
                        Select(
                            Option(
                                "--", disabled=True, selected=(not timeframe), value=""
                            ),
                            Option(
                                "1 week",
                                value="1 week",
                                selected=(timeframe == "1 week"),
                            ),
                            Option(
                                "1 month",
                                value="1 month",
                                selected=(timeframe == "1 month"),
                            ),
                            Option(
                                "3 months",
                                value="3 months",
                                selected=(timeframe == "3 months"),
                            ),
                            Option(
                                "6 months",
                                value="6 months",
                                selected=(timeframe == "6 months"),
                            ),
                            Option(
                                "1 year",
                                value="1 year",
                                selected=(timeframe == "1 year"),
                            ),
                            Option(
                                "3 years",
                                value="3 years",
                                selected=(timeframe == "3 years"),
                            ),
                            Option(
                                "5 years",
                                value="5 years",
                                selected=(timeframe == "5 years"),
                            ),
                            cls="select select-bordered w-full",
                            id="timeframe",
                            name="timeframe",
                        ),
                        P(cls="text-sm opacity-70 mt-1")(
                            "How long are you committing to establishing this habit?",
                        ),
                        # Save Button
                        Div(cls="mt-6 text-right")(
                            Button(
                                "Save Changes",
                                type="submit",
                                cls="btn btn-primary",
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )


def MainContent(user, session):
    user_timezone = session.get("timezone", "UTC")

    return Div(cls="flex flex-col drawer-content h-screen")(
        Div(cls="w-full navbar-center bg-background")(
            Div(cls="flex-none")(
                Label(
                    cls="btn btn-square btn-ghost drawer-button transition-transform",
                    fr="dashboard-drawer",
                    id="drawer-toggle-btn",
                    aria_label="Toggle sidebar",
                )(Lucide("chevron-right")),
            ),
            Div(cls="flex-1 px-2 mx-2 text-4xl text-center font-bold")(H1("Dashboard")),
        ),
        Div(cls="p-4 flex-grow")(
            # Content sections - only one will be visible at a time
            Div(cls="content-section", id="personal-content")(
                H1(cls="text-2xl font-bold")("Personal Settings"),
                PersonalContent(user),
            ),
            Div(cls="content-section hidden", id="habit-content")(
                H1(cls="text-2xl font-bold")("Habit Tracking"),
                HabitContent(user),
            ),
            Div(cls="content-section hidden", id="preferences-content")(
                H1(cls="text-2xl font-bold")("User Preferences"),
                PreferencesContent(user),
            ),
        ),
    )


def DashboardPage(user, session):
    return Div(cls="drawer lg:drawer-open")(
        Input(id="dashboard-drawer", type="checkbox", cls="drawer-toggle"),
        MainContent(user, session),
        Div(cls="drawer-side")(
            Label(
                cls="drawer-overlay", fr="dashboard-drawer", aria_label="close sidebar"
            ),
            SidebarContent(),
        ),
    )


@ar.get("/dashboard")
def get(session):
    user = db.get_user(session["auth"])
    return Title("Dashboard"), DashboardPage(user, session)


@ar.post("/dashboard/update")
async def update_dashboard(request, session):
    """Handle all dashboard updates"""
    try:
        # Get form data
        form_data = await request.form()
        user_email = session["auth"]

        # Get current user data
        current_user = db.get_user(user_email)

        # Create update data starting with current user data
        update_data = dict(current_user) if current_user else {}

        # Convert form data to dict and filter out any special characters in keys
        form_dict = {}
        for key, value in form_data.items():
            # Skip any keys with special characters or empty values
            if key.isalnum() or key in [
                "delivery_time",
                "time_period",
                "habit_details",
                "timeframe",
                "name",
                "bio",
                "formality",
                "assertiveness",
                "intensity",
            ]:
                form_dict[key] = value

        # Update with sanitized form data
        update_data.update(form_dict)

        # Handle special cases for preferences section
        if "delivery_time" in form_data:
            update_data["delivery_time_original"] = form_data["delivery_time"]
            update_data["time_period_original"] = form_data["time_period"]

            # Convert to UTC timestamp
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            timezone = session.get("timezone", "UTC")
            utc_timestamp = convert_local_to_utc(
                today, form_data["delivery_time"], timezone
            )
            update_data["delivery_time_utc"] = utc_timestamp

        # Update user data in database
        success = db.update_user(user_email, update_data)

        if success:
            return RedirectResponse("/dashboard", status_code=303)
        else:
            return "Error saving dashboard information"

    except Exception as e:
        return f"Error saving dashboard information: {str(e)}"


@ar.post("/signout")
def signout(session):
    email = session["auth"]  # Get email before deleting from session
    # Update user's active status to False
    db.update_user(email, {"is_active": False})
    del session["auth"]
    return HttpHeader("HX-Redirect", "/login")


@ar.post("/delete_account")
def delete_account(session):
    if not session.get("auth"):
        return RedirectResponse("/login")

    email = session["auth"]
    try:
        db.delete_user(email)
        del session["auth"]
        return HttpHeader("HX-Redirect", "/")
    except Exception as e:
        return f"Error deleting account: {str(e)}"
