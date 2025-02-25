from fasthtml.common import *
import fasthtml
from monsterui.all import *
from database.dynamo_handler import DynamoHandler
from components import DaisyTopBar

ar = fasthtml.APIRouter()
db = DynamoHandler()


def StepContent(step_num, user):
    """Generate content for each step"""
    match step_num:
        case 1:
            return Fieldset(cls="fieldset bg-card p-4 rounded-box")(
                Legend("Personal Info", cls="fieldset-legend"),
                Label("Full Name", cls="fieldset-label"),
                Input(
                    placeholder="John Doe",
                    id="name",
                    cls="input input-bordered w-full",
                ),
                P(cls="text-sm opacity-70 mt-1")(
                    "This is your display name. You can change this later.",
                ),
            )
        case 2:
            return Fieldset(cls="fieldset bg-card p-4 rounded-box")(
                Legend("Contact Details", cls="fieldset-legend"),
                Label("Phone Number", cls="fieldset-label"),
                Input(
                    placeholder="+1 (555) 000-0000",
                    id="phone",
                    cls="input input-bordered w-full",
                ),
                P(cls="text-sm opacity-70 mt-1")(
                    "We'll use this for important notifications and 2FA.",
                ),
            )
        case 3:
            return Fieldset(cls="fieldset bg-card p-4 rounded-box")(
                Legend("Profile", cls="fieldset-legend"),
                Label("Bio", cls="fieldset-label"),
                TextArea(
                    id="bio",
                    placeholder="Tell us a little bit about yourself",
                    cls="textarea textarea-bordered w-full h-24",
                ),
                P(cls="text-sm opacity-70 mt-1")(
                    "This will be visible on your public profile.",
                ),
            )
        case 4:
            return Fieldset(cls="fieldset bg-card p-4 rounded-box")(
                Legend("Preferences", cls="fieldset-legend"),
                Label("Timezone", cls="fieldset-label"),
                Select(
                    Option("Select timezone", value=""),
                    Option("UTC", value="UTC"),
                    Option("UTC-5", value="UTC-5"),
                    Option("UTC+1", value="UTC+1"),
                    id="timezone",
                    cls="select select-bordered w-full",
                ),
                P(cls="text-sm opacity-70 mt-1")(
                    "Choose your local timezone for accurate scheduling.",
                ),
            )


def SignupForm(user):
    return Div(cls="hero bg-background min-h-screen")(
        Div(cls="container mx-auto")(
            Div(cls="hero-content flex-col")(
                # Progress indicator at top
                Ul(cls="steps w-full mb-8")(
                    Li(cls="step step-primary")("Personal Info", data_content="1"),
                    Li(cls="step")("Contact", data_content="2"),
                    Li(cls="step")("Profile", data_content="3"),
                    Li(cls="step")("Preferences", data_content="4"),
                ),
                # Main form content
                Form(
                    cls="w-full max-w-md", hx_post="/signup/update", hx_trigger="submit"
                )(
                    # Card containing step content
                    Div(cls="card bg-card shadow-lg p-6 w-full")(
                        # Form content wrapper
                        Div(id="form-content")(
                            Hidden(value="1", id="current_step"),
                            Div(id="step-content")(StepContent(1, user)),
                        ),
                        # Navigation footer
                        Div(cls="card-actions justify-end mt-6")(
                            Button(
                                "Back",
                                cls="btn btn-ghost",
                                type="button",
                                hx_post="/signup/nav",
                                hx_vals='{"direction": "prev"}',
                                hx_target="#form-content",
                                hx_swap="innerHTML",
                            ),
                            Button(
                                "Next",
                                cls="btn btn-primary",
                                type="button",
                                hx_post="/signup/nav",
                                hx_vals='{"direction": "next"}',
                                hx_target="#form-content",
                                hx_swap="innerHTML",
                            ),
                        ),
                    )
                ),
            )
        )
    )


@ar.get("/signup")
def get(session):
    if not session.get("auth"):
        return RedirectResponse("/login")
    user = db.get_user(session["auth"])
    return (Title("Complete Your Setup"), SignupForm(user))


@ar.post("/signup/nav")
async def nav(request):
    form = await request.form()
    current_step = int(form.get("current_step", 1))
    direction = form.get("direction")

    # Calculate next step
    next_step = current_step + 1 if direction == "next" else current_step - 1
    next_step = max(1, min(4, next_step))  # Keep between 1-4

    # Return both the new content and the updated step number
    return Div(
        # Hidden input with updated step
        Hidden(value=str(next_step), id="current_step"),
        # New step content
        StepContent(next_step, None),
    )


@ar.post("/signup/update")
async def update(request):
    form = await request.form()
    # Handle form submission and update user profile
    # Redirect to dashboard or next step
    return RedirectResponse("/dashboard")
