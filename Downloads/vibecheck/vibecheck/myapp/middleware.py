import logging, time
from collections import deque
logger = logging.getLogger("requests")
RECENT = deque(maxlen=25)

class RequestLoggingMiddleware:
    def __init__(self, get_response): self.get_response = get_response
    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        ms = round((time.time() - start) * 1000, 1)
        if not request.path.startswith("/static/"):
            logger.info("%s %s -> %s (%sms)", request.method, request.path, response.status_code, ms)
            RECENT.appendleft({"time": time.strftime("%H:%M:%S"), "method": request.method,
                               "path": request.path, "status": response.status_code, "ms": ms})
        return response
