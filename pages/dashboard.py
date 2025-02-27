from fasthtml.common import *
import fasthtml
from monsterui.all import *
from lucide_fasthtml import Lucide
from database.dynamo_handler import DynamoHandler

ar = fasthtml.APIRouter()

### Initialize database
db = DynamoHandler()


def SidebarContent():
    return Div(cls="h-full")(
        Div(cls="text-xl font-bold p-4 border-b")("Settings"),
        Ul(cls="menu p-4 w-80 min-h-full bg-base-200 text-base-content")(
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
                )(Div(cls="flex items-center")(Lucide("calendar", cls="mr-2"), "Habit"))
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
            Div(cls="flex-1 px-2 mx-2 text-xl text-center font-bold")(H1("Dashboard")),
        ),
        Div(cls="p-4 flex-grow")(
            # Content sections - only one will be visible at a time
            Div(cls="content-section", id="personal-content")(
                H1(cls="text-2xl font-bold")("Personal Settings"),
                Div(cls="hero-content text-center")(
                    Div(cls="card w-full bg-background shadow-xl")(
                        Div(cls="card-body")(
                            H1(cls="card-title")("user"),
                            *[P(f"{key}: {value}") for key, value in user.items()],
                        )
                    )
                ),
            ),
            Div(cls="content-section hidden", id="habit-content")(
                H1(cls="text-2xl font-bold")("Habit Tracking"),
                Div(cls="hero-content text-center")(
                    Div(cls="card w-full bg-background shadow-xl")(
                        Div(cls="card-body")(
                            H1(cls="card-title")("session"),
                            *[P(f"{key}: {value}") for key, value in session.items()],
                        )
                    )
                ),
            ),
            Div(cls="content-section hidden", id="preferences-content")(
                H1(cls="text-2xl font-bold")("User Preferences")
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
    return DashboardPage(user, session)
