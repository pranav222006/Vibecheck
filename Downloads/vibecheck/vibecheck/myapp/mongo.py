from datetime import datetime, timezone
from django.conf import settings
_client = None

def get_db():
    global _client
    if not settings.MONGODB_URI: return None
    try:
        from pymongo import MongoClient
        if _client is None:
            _client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=1500)
        return _client["vibecheck"]
    except Exception:
        return None

def save(collection, doc):
    try:
        db = get_db()
        if db is not None:
            doc["created"] = datetime.now(timezone.utc)
            db[collection].insert_one(doc)
            return True
    except Exception:
        pass
    return False

def ping():
    try:
        db = get_db()
        if db is None: return "NOT CONFIGURED"
        db.command("ping"); return "OK"
    except Exception:
        return "DOWN"
