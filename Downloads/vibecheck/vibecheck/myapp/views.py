import json, time, random, requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from . import mongo
from .assistant import respond
from .middleware import RECENT
from .models import FAQ, ErrorCode, Ticket

FALLBACK_QUOTES = [("Happiness is not by chance, but by choice.", "Jim Rohn"),
    ("Almost everything will work again if you unplug it for a few minutes, including you.", "Anne Lamott"),
    ("Rest is not idleness.", "John Lubbock"), ("Energy and persistence conquer all things.", "Benjamin Franklin")]

def home(request): return render(request, "myapp/home.html")

def faqs(request):
    cat = request.GET.get("category", ""); q = request.GET.get("q", "").strip()
    items = FAQ.objects.all()
    if cat: items = items.filter(category=cat)
    if q: items = items.filter(question__icontains=q) | items.filter(answer__icontains=q)
    cats = FAQ.objects.order_by("category").values_list("category", flat=True).distinct()
    return render(request, "myapp/faqs.html", {"faqs": items, "cats": cats, "cat": cat, "q": q})

def errors(request): return render(request, "myapp/errors.html", {"codes": ErrorCode.objects.all()})

def tickets(request):
    sent = None
    if request.method == "POST" and request.POST.get("message"):
        t = Ticket.objects.create(name=request.POST.get("name", "")[:100], email=request.POST.get("email", ""),
            subject=(request.POST.get("subject") or request.POST["message"])[:150], message=request.POST["message"])
        sent = t.id
    return render(request, "myapp/tickets.html", {"tickets": Ticket.objects.all()[:20], "sent": sent})

def fetch_quote():
    start = time.time()
    try:
        r = requests.get("https://zenquotes.io/api/random", timeout=3)
        d = r.json()[0]
        return {"text": d["q"], "author": d["a"], "source": "api"}, round((time.time() - start) * 1000), "OK"
    except Exception:
        t, a = random.choice(FALLBACK_QUOTES)
        return {"text": t, "author": a, "source": "fallback"}, round((time.time() - start) * 1000), "FALLBACK"

def api_quote(request): return JsonResponse(fetch_quote()[0])

@csrf_exempt
@require_POST
def api_chat(request):
    try: data = json.loads(request.body)
    except ValueError: return JsonResponse({"error": "bad request"}, status=400)
    msg = str(data.get("message", "")).strip()[:500]
    if not msg: return JsonResponse({"error": "empty message"}, status=400)
    reply, tid, src = respond(msg)
    mongo.save("chat_logs", {"session": data.get("session", ""), "message": msg, "reply": reply, "source": src, "ticket": tid})
    return JsonResponse({"reply": reply, "ticket": tid, "source": src})

@csrf_exempt
@require_POST
def api_feedback(request):
    try: data = json.loads(request.body)
    except ValueError: return JsonResponse({"error": "bad request"}, status=400)
    ok = mongo.save("feedback", {"session": data.get("session", ""), "message": str(data.get("message", ""))[:500],
                                  "helpful": bool(data.get("helpful"))})
    return JsonResponse({"saved": ok})

def health(request):
    try: sql = "OK" if FAQ.objects.count() >= 0 else "DOWN"
    except Exception: sql = "DOWN"
    _, ms, api = fetch_quote()
    data = {"status": "HEALTHY" if sql == "OK" else "UNHEALTHY", "sql": sql, "mongodb": mongo.ping(),
            "third_party_api": api, "third_party_latency_ms": ms, "time": timezone.now().isoformat()}
    if request.GET.get("format") == "json":
        return JsonResponse(data, status=200 if sql == "OK" else 503)
    return render(request, "myapp/health.html", {"h": data, "logs": list(RECENT)})

def test_error(request):
    code = request.GET.get("code")
    if code == "500": raise RuntimeError("Intentional test error")
    return JsonResponse({"error": "use ?code=500"}, status=418)

def custom_404(request, exception=None): return render(request, "myapp/404.html", status=404)
def custom_500(request): return render(request, "myapp/500.html", status=500)
