from fasthtml.common import *
import fasthtml

# from monsterui.all import *
from database.dynamo_handler import DynamoHandler
from components import DaisyTopBar

ar = fasthtml.APIRouter()
db = DynamoHandler()


def StepContent(step_num, user):
    """Generate content for each step"""
    match step_num:
        case 1:
            return Fieldset(cls="fieldset bg-card p-4 rounded-box")(
                Legend("Profile", cls="fieldset-legend"),
                Label("Name", cls="fieldset-label"),
                Input(cls="input input-bordered w-full")(
                    placeholder="John Doe",
                    id="name",
                ),
                Label("Bio", cls="fieldset-label mt-1"),
                Textarea(cls="textarea textarea-bordered w-full h-24")(
                    placeholder="Tell us a little bit about yourself",
                    id="bio",
                ),
            )
        case 2:
            return Fieldset(cls="fieldset bg-card p-4 rounded-box")(
                Legend("Habit Details", cls="fieldset-legend"),
                Label("What do you want to achieve?", cls="fieldset-label"),
                Textarea(cls="textarea textarea-bordered w-full h-32")(
                    placeholder="Be honest, realistic, and precise.",
                    id="habit_details",
                ),
                Label("Time Frame", cls="fieldset-label"),
                Select(
                    Option("--", disabled=True, selected=True),
                    Option("1 week"),
                    Option("1 month"),
                    Option("3 months"),
                    Option("6 months"),
                    Option("1 year"),
                    Option("3 years"),
                    Option("5 years"),
                    cls="select select-bordered w-full",
                ),
                P(cls="text-sm opacity-70 mt-1")(
                    "How long are you committing to establishing this habit?",
                ),
            )
        case 3:
            return Fieldset(cls="fieldset bg-card p-4 rounded-box")(
                Legend("Preferences", cls="fieldset-legend"),
                Label("Delivery Time", cls="fieldset-label mt-4"),
                Div(cls="join w-full")(
                    Input(
                        type="time",
                        id="delivery_time",
                        value="09:00",
                        cls="input input-bordered join-item w-full",
                    ),
                    Select(
                        Option("AM", value="AM", selected=True),
                        Option("PM", value="PM"),
                        id="time_period",
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
                    ),
                    Div(cls="flex justify-between px-2 text-xs")(
                        Span("Calm & Measured"), Span("Passionate & Energetic")
                    ),
                ),
                P(cls="text-sm opacity-70 mt-4")(
                    "Adjust these sliders to customize the tone and style of your motivational emails.",
                ),
            )


def SignupForm(user):
    return Div(cls="hero bg-background min-h-screen")(
        Div(cls="container mx-auto")(
            Div(cls="hero-content flex-col")(
                # Progress indicator at top
                Ul(cls="steps w-full mb-8")(
                    Li(cls="step step-primary")("Personal Info", data_content="1"),
                    Li(cls="step")("Habit", data_content="2"),
                    Li(cls="step")("Preferences", data_content="3"),
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
