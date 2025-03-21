from fasthtml.common import *
import fasthtml
import datetime
import pytz
import random

from database.dynamo_handler import DynamoHandler
from utils import convert_local_to_utc

db = DynamoHandler()
ar = fasthtml.APIRouter()

steps_dict = {
    1: "Profile",
    2: "Habit",
    3: "Preferences",
}
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


with open(os.path.join(root_dir, "placeholders/habit_details.txt"), "r") as file:
    placeholder_habits = file.readlines()

with open(os.path.join(root_dir, "placeholders/obstacles.txt"), "r") as file:
    placeholder_obstacles = file.readlines()

with open(os.path.join(root_dir, "placeholders/action_plans.txt"), "r") as file:
    placeholder_action_plan = file.readlines()

with open(os.path.join(root_dir, "placeholders/bios.txt"), "r") as file:
    placeholder_bio = file.readlines()


def get_random_placeholders(placeholders: list[str], count: int = 1) -> str:
    """Get random placeholder(s) from a list of strings.
    If count > 1, returns items separated by newlines"""
    # Clean and filter the placeholders
    clean_placeholders = [p.strip() for p in placeholders if p.strip()]

    # Select random items
    selected = random.sample(clean_placeholders, min(count, len(clean_placeholders)))

    # Join with newlines if multiple items
    return "\n".join(selected)


def TextareaWithLimit(
    id: str, name: str, placeholder: str, cls: str = "", required: bool = True
):
    """Create a textarea with character limit counter and validation"""
    return Div(cls="relative")(
        Textarea(
            cls=f"{cls} peer",
            maxlength="500",
            id=id,
            name=name,
            placeholder=placeholder,
            required=required,
            hx_on_input="this.nextElementSibling.textContent = this.value.length + '/500'; this.classList.toggle('textarea-error', this.value.length >= 500)",
        ),
        Div(
            "0/500",
            cls="absolute bottom-1 right-0 text-sm text-base-content/70",
        ),
    )


def StepProgress(step_num: int, steps_dict: dict):
    """Generate step indicator for each step in the signup process"""
    universal_cls = "w-full pt-10 pb-4"

    # Create base steps element
    steps = Ul(cls=f"steps {universal_cls}")

    # Helper function to determine step class
    def get_step_class(step_index):
        if step_index <= step_num:
            return "step-primary"
        return ""

    # Add all steps
    for i in range(1, 4):
        steps(Li(steps_dict[i], cls=f"step {get_step_class(i)}"))

    return steps


def StepContent(step_num: int, steps_dict: dict, session=None):
    """Generate content for each step"""
    fieldset_cls = "fieldset bg-base-100 border border-base-300 p-4 rounded-box"
    textarea_cls = "textarea textarea-bordered w-full h-32 mb-8"  # Increased margin bottom to accommodate counter
    tooltip_cls = "tooltip tooltip-info"
    match step_num:
        case 1:
            # Get email from session if available
            email = session.get("auth", "") if session else ""

            return Fieldset(
                cls=fieldset_cls,
            )(
                Legend(steps_dict[1], cls="fieldset-legend"),
                # Add email as a hidden field instead of visible input
                Hidden(value=email, name="email") if email else None,
                Div(
                    cls="text-sm mb-4",
                    id="signed-in-as",
                )(
                    P("Signed in as"),
                    P(cls="text-secondary")(
                        f"{email}" if email else "Email not found in session",
                    ),
                ),
                Div(
                    cls=tooltip_cls,
                    data_tip="How do you want to be called?",
                )(Label("Name", cls="fieldset-label")),
                Input(cls="input input-bordered w-full mb-4")(
                    placeholder="John Doe",
                    id="name",
                    name="name",
                    required=True,
                ),
                Div(cls="text-error text-sm hidden", id="name-error")(
                    "Name is required"
                ),
                Div(
                    cls=tooltip_cls,
                    data_tip="Tell us a little about yourself, be as brief or as detailed as you want.",
                )(Label("Bio", cls="fieldset-label")),
                TextareaWithLimit(
                    id="bio",
                    name="bio",
                    placeholder=get_random_placeholders(placeholder_bio),
                    cls=textarea_cls,
                ),
                Div(cls="text-error text-sm hidden", id="bio-error")("Bio is required"),
            )
        case 2:
            error_cls = "text-error text-sm hidden"
            return Fieldset(
                cls=fieldset_cls,
            )(
                Legend(steps_dict[2], cls="fieldset-legend"),
                Div(
                    cls=tooltip_cls,
                    data_tip="What do you want to achieve? Be honest, realistic, and precise.",
                )(Label("Details", cls="fieldset-label")),
                TextareaWithLimit(
                    id="habit_details",
                    name="habit_details",
                    placeholder=get_random_placeholders(placeholder_habits),
                    cls=textarea_cls,
                ),
                Div(cls=error_cls, id="habit_details-error")("This field is required"),
                Div(
                    cls=tooltip_cls,
                    data_tip="How are you actually going to achieve this?",
                )(Label("Action Plan", cls="fieldset-label")),
                TextareaWithLimit(
                    id="action_plan",
                    name="action_plan",
                    placeholder=get_random_placeholders(placeholder_action_plan, 1),
                    cls=textarea_cls,
                ),
                Div(cls=error_cls, id="action_plan-error")("Action Plan is required"),
                Div(
                    cls=tooltip_cls,
                    data_tip="What might stop you from forming this habit?",
                )(Label("Potential Obstacles", cls="fieldset-label")),
                TextareaWithLimit(
                    id="obstacles",
                    name="obstacles",
                    placeholder=get_random_placeholders(placeholder_obstacles, 3),
                    cls=textarea_cls,
                ),
                Div(cls=error_cls, id="obstacles-error")(
                    "Nothing's going to stop you?! Great! Put that."
                ),
            )
        case 3:
            return Fieldset(
                cls=fieldset_cls,
            )(
                Legend(steps_dict[3], cls="fieldset-legend"),
                Div(
                    cls=tooltip_cls,
                    data_tip="When would you like to receive your daily motivation?",
                )(Label("Delivery Time", cls="fieldset-label mt-4")),
                Input(
                    type="time",
                    id="delivery_time",
                    name="delivery_time",
                    value="09:00",
                    cls="input input-bordered w-full",
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

    # Next/Submit button - will be enabled/disabled by JavaScript
    if step_num < 3:
        nav_buttons(
            Button("Next", cls="btn btn-primary", type="submit", id="next-button")
        )
    else:
        nav_buttons(
            Button("Submit", cls="btn btn-success", type="submit", id="next-button")
        )

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
    # Create container using hero component for full-height background
    return Title("Sign Up"), Div(cls="hero min-h-screen bg-base-200")(
        Div(cls="hero-content flex-col w-full max-w-md p-0")(
            # Fixed progress indicator at the top
            Div(
                cls="w-full sticky top-0 bg-base-200 z-10",
                id="progress-indicator",
            )(
                StepProgress(step_num, steps_dict),
            ),
            # Form container
            Div(cls="w-full", id="signup-container")(
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

    return Title("Sign Up"), SignUpPage(
        step_num=1, form_data=form_data, session=session
    )


# Process form submission for each step
@ar.post("/signup/process/{step}")
async def process_step(request, step: int, session):
    """Process form data for the current step and move to next step"""
    # Get the form data
    form_data = await request.form()

    # Convert form data to dict and filter out unused fields
    form_dict = {
        key: value
        for key, value in form_data.items()
        if key
        in [
            "email",
            "name",
            "bio",
            "habit_details",
            "action_plan",
            "obstacles",
            "delivery_time",
        ]
    }

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
            if "delivery_time" in user_data:
                # Get delivery time and timezone
                delivery_time = user_data["delivery_time"]  # Format: HH:MM
                timezone = session.get("timezone", "UTC")

                # Parse the delivery time
                hour, minute = map(int, delivery_time.split(":"))

                # Get current time in user's timezone
                user_tz = pytz.timezone(timezone)
                now = datetime.datetime.now(user_tz)

                # Create a datetime for today at the delivery time in user's timezone
                today_delivery = now.replace(
                    hour=hour, minute=minute, second=0, microsecond=0
                )

                # If delivery time is in the past, set for tomorrow
                if today_delivery < now:
                    next_email_date = today_delivery + datetime.timedelta(days=1)
                else:
                    next_email_date = today_delivery

                # Convert next_email_date to UTC before saving
                next_email_date_utc = next_email_date.astimezone(pytz.UTC)
                user_data["next_email_date"] = next_email_date_utc.isoformat()

                # Convert delivery time to UTC for storage
                utc_time = convert_local_to_utc(delivery_time, timezone)
                user_data["delivery_time_utc"] = utc_time
                user_data.pop("delivery_time", None)

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
    return Div(cls="container mx-auto max-w-md p-4")(
        Div(
            cls="text-center p-8 bg-base-100 border border-base-300 rounded-box shadow-lg"
        )(
            H2("Thank You for Signing Up!", cls="text-2xl font-bold"),
            P(cls="my-4")("Your account has been created successfully."),
            P(cls="mb-4")(
                "You will receive your first motivational message according to your preferences."
            ),
            # Use onclick with JavaScript redirect instead of hx_get
            A("Go to Dashboard", cls="btn btn-primary", href="/dashboard"),
        ),
    )
