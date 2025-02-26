from fasthtml.common import *
import fasthtml
import datetime

# from monsterui.all import *
import monsterui.all as mui

from database.dynamo_handler import DynamoHandler
from utils import convert_local_to_utc

db = DynamoHandler()
ar = fasthtml.APIRouter()

steps_dict = {
    1: "Profile",
    2: "Habit",
    3: "Preferences",
}


def StepProgress(step_num: int, steps_dict: dict):
    """Generate step indicator for each step in the signup process"""
    universal_cls = "w-full py-4"
    match step_num:
        case 1:
            return mui.Steps(cls=universal_cls)(
                mui.LiStep(steps_dict[1], cls=mui.StepT.primary),
                mui.LiStep(steps_dict[2], cls=mui.StepT.neutral),
                mui.LiStep(steps_dict[3], cls=mui.StepT.neutral),
            )
        case 2:
            return mui.Steps(cls=universal_cls)(
                mui.LiStep(steps_dict[1], cls=mui.StepT.primary),
                mui.LiStep(steps_dict[2], cls=mui.StepT.primary),
                mui.LiStep(steps_dict[3], cls=mui.StepT.neutral),
            )
        case 3:
            return mui.Steps(cls=universal_cls)(
                mui.LiStep(steps_dict[1], cls=mui.StepT.primary),
                mui.LiStep(steps_dict[2], cls=mui.StepT.primary),
                mui.LiStep(steps_dict[3], cls=mui.StepT.primary),
            )


def StepContent(step_num: int, steps_dict: dict, session=None):
    """Generate content for each step"""
    match step_num:
        case 1:
            # Get email from session if available
            email = session.get("auth", "") if session else ""

            return Fieldset(cls="fieldset bg-card p-4 rounded-box")(
                Legend(steps_dict[1], cls="fieldset-legend"),
                # Add email as a hidden field instead of visible input
                Hidden(value=email, name="email") if email else None,
                P(cls="text-sm mb-4")(
                    f"Signed in as {email}" if email else "Email not found in session"
                ),
                Label("Name", cls="fieldset-label"),
                Input(cls="input input-bordered w-full")(
                    placeholder="John Doe",
                    id="name",
                    name="name",
                ),
                Label("Bio", cls="fieldset-label mt-1"),
                Textarea(cls="textarea textarea-bordered w-full h-24")(
                    placeholder="Tell us a little bit about yourself",
                    id="bio",
                    name="bio",
                ),
            )
        case 2:
            return Fieldset(cls="fieldset bg-card p-4 rounded-box")(
                Legend(steps_dict[2], cls="fieldset-legend"),
                Label("What do you want to achieve?", cls="fieldset-label"),
                Textarea(cls="textarea textarea-bordered w-full h-32")(
                    placeholder="Be honest, realistic, and precise.",
                    id="habit_details",
                    name="habit_details",
                ),
                Label("Time Frame", cls="fieldset-label"),
                Select(
                    Option("--", disabled=True, selected=True, value=""),
                    Option("1 week", value="1 week"),
                    Option("1 month", value="1 month"),
                    Option("3 months", value="3 months"),
                    Option("6 months", value="6 months"),
                    Option("1 year", value="1 year"),
                    Option("3 years", value="3 years"),
                    Option("5 years", value="5 years"),
                    cls="select select-bordered w-full",
                    id="timeframe",
                    name="timeframe",
                ),
                P(cls="text-sm opacity-70 mt-1")(
                    "How long are you committing to establishing this habit?",
                ),
            )
        case 3:
            return Fieldset(cls="fieldset bg-card p-4 rounded-box")(
                Legend(steps_dict[3], cls="fieldset-legend"),
                Label("Delivery Time", cls="fieldset-label mt-4"),
                Div(cls="join w-full")(
                    Input(
                        type="time",
                        id="delivery_time",
                        name="delivery_time",
                        value="09:00",
                        cls="input input-bordered join-item w-full",
                    ),
                    Select(
                        Option("AM", value="AM", selected=True),
                        Option("PM", value="PM"),
                        id="time_period",
                        name="time_period",
                        cls="select select-bordered join-item",
                    ),
                ),
                P(cls="text-sm opacity-70 mt-1")(
                    "When would you like to receive your daily motivation?",
                ),
                Label("Email Style", cls="fieldset-label mt-4"),
                # Formality Slider
                Label("Formality", cls="label mt-4"),
                Div(cls="w-full")(
                    Input(
                        type="range",
                        min="0",
                        max="100",
                        value="50",
                        cls="range range-primary",
                        id="formality",
                        name="formality",
                    ),
                    Div(cls="flex justify-between px-2 text-xs")(
                        Span("Casual & Friendly"), Span("Formal & Professional")
                    ),
                ),
                # Assertiveness Slider
                Label("Assertiveness", cls="label mt-4"),
                Div(cls="w-full")(
                    Input(
                        type="range",
                        min="0",
                        max="100",
                        value="50",
                        cls="range range-secondary",
                        id="assertiveness",
                        name="assertiveness",
                    ),
                    Div(cls="flex justify-between px-2 text-xs")(
                        Span("Gentle & Supportive"), Span("Direct & Challenging")
                    ),
                ),
                # Intensity Slider
                Label("Emotional Intensity", cls="label mt-4"),
                Div(cls="w-full")(
                    Input(
                        type="range",
                        min="0",
                        max="100",
                        value="50",
                        cls="range range-accent",
                        id="intensity",
                        name="intensity",
                    ),
                    Div(cls="flex justify-between px-2 text-xs")(
                        Span("Calm & Measured"), Span("Passionate & Energetic")
                    ),
                ),
                P(cls="text-sm opacity-70 mt-4")(
                    "Adjust these sliders to customize the tone and style of your motivational emails.",
                ),
            )


def SignUpForm(step_num: int, form_data=None, session=None):
    """Form container with navigation buttons and content for current step"""
    # Default values for the form fields
    defaults = form_data or {}

    # Generate the content for the current step, passing session
    step_content = StepContent(step_num, steps_dict, session)

    # Fill the form with any existing data if provided
    if form_data:
        form = fill_form(step_content, defaults)
    else:
        form = step_content

    # Add navigation buttons based on current step
    nav_buttons = Div(cls="flex justify-between mt-6")

    # Back button for steps 2 and 3
    if step_num > 1:
        nav_buttons(
            Button(
                "Back",
                cls="btn btn-outline",
                hx_post=f"/signup/step/{step_num-1}",
                hx_trigger="click",
                hx_target="#form-content",
                hx_swap="innerHTML",
            )
        )
    else:
        nav_buttons(Div())  # Empty div as placeholder

    # Next/Submit button
    if step_num < 3:
        nav_buttons(Button("Next", cls="btn btn-primary", type="submit"))
    else:
        nav_buttons(Button("Submit", cls="btn btn-success", type="submit"))

    # Create the form with the current step content and navigation
    return Form(
        id="signup-form",
        hx_post=f"/signup/process/{step_num}",
        hx_target="#form-content",
        hx_swap="innerHTML",
    )(
        # Add a hidden field to track the current step
        Hidden(value=str(step_num), name="current_step"),
        form,
        nav_buttons,
    )


def SignUpPage(step_num=1, form_data=None, session=None):
    """Complete signup page with progress indicator and form"""
    # Create container with fixed progress at top and scrollable form below
    return mui.Titled(
        f"Sign Up - {steps_dict[step_num]}",
        Div(cls="container mx-auto max-w-md")(
            # Fixed progress indicator at the top
            Div(
                cls="sticky top-0 bg-background z-10 shadow-sm", id="progress-indicator"
            )(
                StepProgress(step_num, steps_dict),
            ),
            # Form container with padding
            Div(cls="p-4", id="signup-container")(
                # Container for form content that will be updated by HTMX
                Div(id="form-content")(
                    SignUpForm(step_num, form_data, session),
                ),
            ),
        ),
    )


@ar.get("/signup")
def get(session=None):
    """Initial signup page (step 1)"""
    # Get any previously stored form data from session
    form_data = session.get("signup_data", {})

    # If user is not authenticated, redirect to login
    if not session or "auth" not in session:
        return RedirectResponse("/login")

    return SignUpPage(step_num=1, form_data=form_data, session=session)


# Process form submission for each step
@ar.post("/signup/process/{step}")
async def process_step(request, step: int, session):
    """Process form data for the current step and move to next step"""
    # Get the form data
    form_data = await request.form()

    # Convert form data to dict
    form_dict = dict(form_data)

    # Initialize signup data in session if not exists
    if "signup_data" not in session:
        session["signup_data"] = {}

    # Update session with current form data
    session["signup_data"].update(form_dict)

    # Determine next step
    if step < 3:
        # Move to next step
        next_step = step + 1

        # Return HTML with HX-Trigger to perform a full page refresh to the next step
        # This avoids the duplication issue completely
        return Div(
            Script(
                """
                // Redirect to the next step with all session data preserved
                window.location.href = '/signup/render/' + """
                + str(next_step)
                + """;
            """
            ),
            id="form-content",
        )
    else:
        # Final step - save to database
        try:
            # Extract all form data from session
            user_data = session["signup_data"]

            # Process delivery time to convert to UTC format
            if "delivery_time" in user_data and "time_period" in user_data:
                # Get delivery time components
                delivery_time = user_data["delivery_time"]  # Format: HH:MM
                time_period = user_data["time_period"]  # AM or PM

                # Convert 12-hour format to 24-hour if needed
                hour, minute = map(int, delivery_time.split(":"))
                if time_period == "PM" and hour < 12:
                    hour += 12
                elif time_period == "AM" and hour == 12:
                    hour = 0

                # Format as 24-hour time
                delivery_time_24h = f"{hour:02d}:{minute:02d}"

                # Get current date in YYYY-MM-DD format
                today = datetime.datetime.now().strftime("%Y-%m-%d")

                # Get user's timezone from session
                timezone = session.get("timezone", "UTC")

                # Convert to UTC
                utc_timestamp = convert_local_to_utc(today, delivery_time_24h, timezone)

                # Update user data with UTC timestamp
                user_data["delivery_time_utc"] = utc_timestamp

                # Keep original values for reference if needed
                user_data["delivery_time_original"] = delivery_time
                user_data["time_period_original"] = time_period

            # Save to database - using correct method name
            db.create_user(user_data)

            # Clear session data after successful submission
            session.pop("signup_data", None)

            # Redirect to success page
            return RedirectResponse("/signup/success", status_code=303)
        except Exception as e:
            # Handle errors
            return Div(cls="text-center p-4", id="form-content")(
                H2("Something went wrong", cls="text-2xl font-bold text-error"),
                P(cls="my-4")(f"Error: {str(e)}"),
                Button("Try Again", cls="btn btn-primary mt-4", hx_get="/signup"),
            )


# Handle back button navigation
@ar.post("/signup/step/{step}")
def navigate_to_step(step: int, session):
    """Navigate to a specific step using JavaScript redirect"""
    return Div(
        Script(
            f"""
            // Redirect to the specified step with all session data preserved
            window.location.href = '/signup/render/{step}';
        """
        ),
        id="form-content",
    )


# New endpoint to render a specific step
@ar.get("/signup/render/{step}")
def render_step(step: int, session):
    """Render a specific step of the signup form"""
    # Get stored form data
    form_data = session.get("signup_data", {})

    # Return the full page for the requested step with stored data
    return SignUpPage(step_num=step, form_data=form_data, session=session)


# Success page after completion
@ar.get("/signup/success")
def success():
    """Display success message after completing signup"""
    return Titled(
        "Signup Complete",
        Div(cls="container mx-auto max-w-md p-4")(
            Div(cls="text-center p-8 bg-card rounded-box shadow-lg")(
                H2("Thank You for Signing Up!", cls="text-2xl font-bold"),
                P(cls="my-4")("Your account has been created successfully."),
                P(cls="mb-4")(
                    "You will receive your first motivational message according to your preferences."
                ),
                # Use onclick with JavaScript redirect instead of hx_get
                A("Go to Dashboard", cls="btn btn-primary", href="/dashboard"),
            ),
        ),
    )
