"""Localhost protection for the single-user prototype (CR-02, decision D10).

There is no login, so the server itself must refuse requests that don't come from
this app on this MacBook:

1. ``TrustedHostMiddleware``: only ``localhost`` / ``127.0.0.1`` / ``[::1]`` Host headers
   (blocks DNS-rebinding attacks).
2. ``RequireWriteHeaderMiddleware``: POST/PUT/PATCH/DELETE must carry
   ``X-Fitting-Room: 1``. Browsers only let another website send a custom header after a
   CORS preflight, and this server has no CORS, so other sites can't change data.

The server must also listen on 127.0.0.1 only (see the ``dev:api`` script).
"""

from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

WRITE_HEADER = "x-fitting-room"
WRITE_HEADER_VALUE = "1"
WRITE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]


class RequireWriteHeaderMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http" and scope["method"] in WRITE_METHODS:
            headers = dict(scope["headers"])
            if headers.get(WRITE_HEADER.encode()) != WRITE_HEADER_VALUE.encode():
                response = JSONResponse(
                    {"detail": "Missing X-Fitting-Room header"}, status_code=403
                )
                await response(scope, receive, send)
                return
        await self.app(scope, receive, send)


def protect(app: ASGIApp) -> None:
    """Install both protections on a FastAPI/Starlette app (host check runs first)."""
    app.add_middleware(RequireWriteHeaderMiddleware)  # type: ignore[attr-defined]
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)  # type: ignore[attr-defined]
