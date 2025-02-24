from fasthtml.common import *
import fasthtml
from monsterui.all import *

ar = fasthtml.APIRouter()


@ar.get("/dashboard")
def get():
    return H1("Dashboard")
