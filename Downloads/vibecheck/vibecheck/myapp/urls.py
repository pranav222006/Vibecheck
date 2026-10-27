from django.urls import path
from . import views as v
urlpatterns = [
    path("", v.home, name="home"), path("faqs/", v.faqs, name="faqs"), path("errors/", v.errors, name="errors"),
    path("tickets/", v.tickets, name="tickets"), path("health/", v.health, name="health"),
    path("api/chat/", v.api_chat), path("api/feedback/", v.api_feedback), path("api/quote/", v.api_quote),
    path("test-error/", v.test_error),
]
