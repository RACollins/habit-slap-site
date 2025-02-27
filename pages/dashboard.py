from fasthtml.common import *
import fasthtml
from monsterui.all import *
from lucide_fasthtml import Lucide

ar = fasthtml.APIRouter()


def SidebarContent():
    return Div(cls="h-full")(
        Div(cls="text-xl font-bold p-4 border-b")("Settings"),
        Ul(cls="menu p-4 w-80 min-h-full bg-base-200 text-base-content")(
            Li()(
                A(
                    cls="sidebar-link",
                    href="#personal",
                    data_target="personal-content",
                )(
                    Div(cls="flex items-center")(
                        Lucide("user", cls="mr-2"), "Personal"
                    )
                )
            ),
            Li()(
                A(
                    cls="sidebar-link",
                    href="#habit",
                    data_target="habit-content",
                )(
                    Div(cls="flex items-center")(
                        Lucide("calendar", cls="mr-2"), "Habit"
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
        ),
    )


def MainContent():
    return Div(cls="flex flex-col drawer-content h-screen")(
        Div(cls="w-full navbar bg-background")(
            Div(cls="flex-none")(
                Label(
                    cls="btn btn-square btn-ghost drawer-button transition-transform",
                    fr="dashboard-drawer",
                    id="drawer-toggle-btn",
                    aria_label="Toggle sidebar",
                )(
                    Lucide("chevron-right")
                ),
            ),
            Div(cls="flex-1 px-2 mx-2 text-xl font-bold")("Dashboard"),
        ),
        Div(cls="p-4 flex-grow")(
            # Content sections - only one will be visible at a time
            Div(cls="content-section", id="personal-content")(
                H1(cls="text-2xl font-bold")("Personal Settings")
            ),
            Div(cls="content-section hidden", id="habit-content")(
                H1(cls="text-2xl font-bold")("Habit Tracking")
            ),
            Div(cls="content-section hidden", id="preferences-content")(
                H1(cls="text-2xl font-bold")("User Preferences")
            ),
        ),
    )


def DashboardPage():
    return Div(cls="drawer lg:drawer-open")(
        Input(id="dashboard-drawer", type="checkbox", cls="drawer-toggle"),
        MainContent(),
        Div(cls="drawer-side")(
            Label(
                cls="drawer-overlay",
                fr="dashboard-drawer", 
                aria_label="close sidebar"
            ),
            SidebarContent(),
        ),
    )


@ar.get("/dashboard")
def get():
    return DashboardPage()
