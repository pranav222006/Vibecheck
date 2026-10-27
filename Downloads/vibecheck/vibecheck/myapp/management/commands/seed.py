from django.core.management.base import BaseCommand
from myapp.models import FAQ, ErrorCode

FAQS = [
 ("General", "What is Vibe Check?", "Vibe Check is a mood board: pick a mood and the page changes its colours, background, quote and music."),
 ("General", "Is Vibe Check free to use?", "Yes, everything on the site is free and needs no sign-up."),
 ("General", "Does it work on mobile?", "Yes. The layout is responsive and works on phones, tablets and desktops."),
 ("Vibes", "Which moods are available?", "Happy, Stressed, Sleepy and Hyped. Each has its own theme and Spotify playlist."),
 ("Vibes", "How do I change my vibe?", "Tap any mood button on the home page. The theme switches instantly."),
 ("Vibes", "Where do the quotes come from?", "From a third-party quote API. If it is slow or down, a built-in quote is shown instead."),
 ("Music", "Why does the Spotify player not play full songs?", "Spotify embeds play 30-second previews unless you are logged in to Spotify in the same browser."),
 ("Music", "Can I change the playlists?", "Not yet. Playlists are fixed per mood, and this is a planned improvement."),
 ("Account", "Do I need an account?", "No account is needed. Support tickets only ask for an optional name and email."),
 ("Support", "How do I contact support?", "Use the Support Tickets page or just ask the chat assistant. If it cannot answer, it opens a ticket for you."),
 ("Technical", "How is my data stored?", "Tickets are stored in an SQL database. Chat logs and feedback are stored in MongoDB."),
 ("Technical", "What does the health page show?", "It shows the status of the SQL database, MongoDB, the quote API latency and recent HTTP requests."),
]
ERRORS = [
 (400, "Bad Request", "The server could not understand the request.", "Check the URL or form data and try again."),
 (401, "Unauthorized", "Authentication is required and was missing or invalid.", "Sign in again or supply valid credentials."),
 (403, "Forbidden", "You do not have permission to view this resource.", "Ask the site owner for access."),
 (404, "Not Found", "The page you requested does not exist.", "Check the address or go back to the home page."),
 (418, "Vibe Mismatch", "Site-specific code: the requested vibe is not one we serve.", "Pick one of Happy, Stressed, Sleepy or Hyped."),
 (429, "Too Many Requests", "You sent too many requests in a short time.", "Wait a minute and try again."),
 (500, "Internal Server Error", "Something went wrong on our side.", "Reload the page. If it persists, ask the assistant to open a ticket."),
 (503, "Service Unavailable", "The server is temporarily overloaded or under maintenance.", "Try again in a few minutes."),
]
class Command(BaseCommand):
    def handle(self, *a, **k):
        if not FAQ.objects.exists():
            FAQ.objects.bulk_create([FAQ(category=c, question=q, answer=a) for c, q, a in FAQS])
        for code, t, e, f in ERRORS:
            ErrorCode.objects.get_or_create(code=code, defaults=dict(title=t, explanation=e, fix=f))
        self.stdout.write("Seeded.")
