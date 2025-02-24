from fasthtml.common import *
import fasthtml
from monsterui.all import *

ar = fasthtml.APIRouter()


@ar.get("/signup")
def get():
    return H1("Signup")
