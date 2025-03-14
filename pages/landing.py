from fasthtml.common import *
import fasthtml
from components import (
    DaisyTopBar,
    HowItWorksCard,
    TestimonialCard,
    FAQComp,
    PricingCard,
)
from lucide_fasthtml import Lucide


ar = fasthtml.APIRouter()


def MainSignUp():
    return Div(cls="hero bg-base-300 min-h-screen")(
        Div(cls="hero-content text-center")(
            Div(cls="max-w-md")(
                H1("Habit Slap", cls="text-base-content text-5xl font-bold"),
                P(cls="flex items-center justify-center gap-2 py-3 text-base-content")(
                    "Motivation like a slap in the face",
                    Lucide("hand", cls="text-primary"),
                    Lucide("sparkles", cls="text-primary"),
                ),
                A(
                    Button(
                        "Get Started",
                        cls="btn btn-primary text-primary-content py-3",
                    ),
                    href="/login",
                ),
                P("Scroll down to learn more", cls="text-secondary py-3"),
                A(
                    "↓",
                    href="#how-it-works",
                    cls="text-2xl bounce-animation scroll-smooth",
                ),
            ),
        ),
    )


def HowItWorks():
    card_content = {
        "step1": {
            "top": "Step 1",
            "body": "🎯 Set a Goal",
            "bottom": "Sign up with your email and set a goal.",
        },
        "step2": {
            "top": "Step 2",
            "body": "💪 Get Motivated",
            "bottom": "Recieve daily emails with motivational messages tailored to you.",
        },
        "step3": {
            "top": "Step 3",
            "body": "🏅 Get Sh*t Done!",
            "bottom": "No more excuses! Build that habit! Attack your week! Also works well for quitting bad habits.",
        },
    }
    return Div(cls="container mx-auto py-16 bg-base-300", id="how-it-works")(
        H2(
            "How it Works", cls="text-4xl font-bold text-center mb-12 text-base-content"
        ),
        Div(cls="flex flex-col md:flex-row gap-8 justify-center items-stretch px-4")(
            *[HowItWorksCard(card_content[f"step{i+1}"]) for i in range(3)],
        ),
    )


def Testimonials():
    testimonials = [
        {
            "text": "I used to smoke like a chimney before I signed up to Habit Slap. "
            "You couldn't stop me! One after the other, puff, puff, puffing away. "
            "Tommy Tank they used to call me, which I didn't like because that's not my name. "
            "But getting those emails every morning, it's like the cigarette was being slapped right out of my mouth! ",
            "author": "Thomas Walker",
            "username": "tommychoochoowalker",
        },
        {
            "text": "New morning routine: wake up, read email, lock the f*ck in!",
            "author": "Xavier Wickman",
            "username": "saltybread",
        },
        {
            "text": "I look forward to the emails every day. "
            "It's exciting! "
            "Not like that drop-of-the-stomach kind of feeling you get from not realising there's another step before the end of the stair case. "
            "More like that slow burn excitement, "
            "like waiting for your meal kit delivery.",
            "author": "Hannah Rowley",
            "username": "theforestgirl",
        },
        {
            "text": "I'd been meaning to read 12 books a day ever since I was a kid. "
            "But I never could get myself to do it. "
            "Until I started getting these emails every day. "
            "Now I'm reading 12 books a day, and I'm not even trying! "
            "It's like the books are just flying into my brain! ",
            "author": "Mike Rodriguez",
            "username": "mikedev",
        },
        {
            "text": "Wow... I never knew I needed this in my life, "
            "but I'm absolutely addicted. "
            "Motivation up the wazoo!",
            "author": "Sarah Chen",
            "username": "sarahcodes",
        },
        {
            "text": "I've tried many habit tracking apps, "
            "but the email slaps really make a difference. "
            "They're like having a friend who won't let you slack off.",
            "author": "Peter Pickering",
            "username": "peterpickedapieceofpickledpepper",
        },
    ]

    return Div(cls="container mx-auto py-16 px-4 bg-base-300")(
        H2("Testimonials", cls="text-4xl font-bold text-center mb-4 text-base-content"),
        P(
            "What our users are saying about us (may be fake)",
            cls="text-center text-base-content mb-12",
        ),
        Div(cls="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-3 gap-8")(
            *[
                TestimonialCard(
                    text=t["text"], author=t["author"], username=t["username"]
                )
                for t in testimonials
            ],
        ),
    )


def FAQ():
    faq_content = {
        "who": {
            "question": "Who is this for?",
            "answer": "For those who want to improve, know how to do it, but lack the motivation to do it.",
        },
        "cost": {
            "question": "How much does it cost?",
            "answer": "It's free! Sign up with your email and set a goal. Cancel anytime.",
        },
        "writers": {
            "question": "Who writes the emails?",
            "answer": "gpt-4o-mini, but working on a custom model, and even human written emails (coming soon!)",
        },
        "frequency": {
            "question": "How often will I recieve emails?",
            "answer": "Every day, but you can change this in your dashboard.",
        },
    }
    return Div(cls="container mx-auto py-16 px-4 bg-base-300")(
        H2("FAQ", cls="text-4xl font-bold text-center mb-8 text-base-content"),
        Div(cls="space-y-4")(
            *[
                FAQComp(qa_dict["question"], qa_dict["answer"])
                for k, qa_dict in faq_content.items()
            ],
        ),
    )


def Pricing():
    return Div(cls="container mx-auto py-16 px-4 bg-base-300")(
        H2("Pricing", cls="text-4xl font-bold text-center mb-8 text-base-content"),
        Div(cls="flex flex-col md:flex-row gap-8 justify-center items-stretch")(
            PricingCard("Free", "$0", ["1 goal", "Daily emails", "No commitment"]),
            PricingCard("Premium", "$10", ["1 goal", "Daily emails", "No commitment"]),
            PricingCard("Human", "$100", ["1 goal", "Daily emails", "No commitment"]),
        ),
    )


@ar.get("/")
def get():
    return (
        Title("Habit Slap"),
        Style("html { scroll-behavior: smooth; }"),
        DaisyTopBar(),
        MainSignUp(),
        HowItWorks(),
        Div(cls="mx-16")(Div(cls="divider")),
        Testimonials(),
        Div(cls="mx-16")(Div(cls="divider")),
        FAQ(),
        Div(cls="mx-16")(Div(cls="divider")),
        Pricing(),
    )
