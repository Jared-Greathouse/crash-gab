import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("performance")

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = (time.time() - start) * 1000  # ms
        logger.info(f"{request.method} {request.url.path} took {duration:.2f} ms")
        return response