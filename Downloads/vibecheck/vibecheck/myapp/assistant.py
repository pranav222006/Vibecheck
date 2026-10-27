import re, requests
from django.conf import settings
from .models import FAQ, ErrorCode, Ticket

STOP = set("a an the is are do does i my me to of in on for and or how what can it this that you your with".split())
def tokens(s): return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP}

def best_faq(msg):
    q = tokens(msg)
    if not q: return None
    best, score = None, 0
    for f in FAQ.objects.all():
        s = len(q & tokens(f.question + " " + f.answer)) / len(q)
        if s > score: best, score = f, s
    return best if score >= 0.5 else None

def llm_answer(msg):
    if not settings.ANTHROPIC_API_KEY: return None
    ctx = "\n".join(f"Q: {f.question} A: {f.answer}" for f in FAQ.objects.all())
    try:
        r = requests.post("https://api.anthropic.com/v1/messages", timeout=8,
            headers={"x-api-key": settings.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01"},
            json={"model": "claude-sonnet-4-6", "max_tokens": 300,
                  "system": "Answer ONLY using these FAQs. If they don't contain the answer, reply exactly NO_ANSWER.\n" + ctx,
                  "messages": [{"role": "user", "content": msg}]})
        text = r.json()["content"][0]["text"].strip()
        return None if "NO_ANSWER" in text else text
    except Exception:
        return None

def respond(msg):
    """Returns (reply, ticket_id or None, source)."""
    m = re.search(r"\b(400|401|403|404|418|429|500|503)\b", msg)
    if m:
        e = ErrorCode.objects.filter(code=int(m.group(1))).first()
        if e: return f"Error {e.code} – {e.title}: {e.explanation} Fix: {e.fix}", None, "error_code"
    f = best_faq(msg)
    if f: return f.answer, None, "faq"
    text = llm_answer(msg)
    if text: return text, None, "llm"
    t = Ticket.objects.create(subject=msg[:100], message=msg, source="chat")
    return f"I couldn't find an answer, so I've opened support ticket #{t.id} for you. Our team will follow up.", t.id, "ticket"
