"""Language Detection Middleware for gateway."""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from shared.i18n.translation import SUPPORTED_LANGUAGES


def resolve_request_language(request: Request) -> str:
    """Extract requested language using 5-level detection priority."""
    path = request.url.path.strip("/")
    parts = path.split("/")

    # Level 1: URL path prefix (e.g., /hi/kundali -> 'hi')
    if parts and parts[0] in SUPPORTED_LANGUAGES:
        return parts[0]

    # Level 2: Query parameter (?lang=hi)
    query_lang = request.query_params.get("lang", "").lower().strip()
    if query_lang in SUPPORTED_LANGUAGES:
        return query_lang

    # Level 3: Cookie (lang=hi)
    cookie_lang = request.cookies.get("lang", "").lower().strip()
    if cookie_lang in SUPPORTED_LANGUAGES:
        return cookie_lang

    # Level 4: Accept-Language header
    accept_lang = request.headers.get("accept-language", "")
    if accept_lang:
        for item in accept_lang.split(","):
            raw_lang = item.split(";")[0].strip().lower()
            code = raw_lang.split("-")[0]
            if code in SUPPORTED_LANGUAGES:
                return code

    # Level 5: Default fallback
    return "en"


class LanguageDetectionMiddleware(BaseHTTPMiddleware):
    """Middleware extracting language preference and setting request.state.lang."""

    async def dispatch(self, request: Request, call_next):
        lang = resolve_request_language(request)
        request.state.lang = lang
        response = await call_next(request)

        # Set lang cookie if not explicitly set or mismatched
        if request.cookies.get("lang") != lang:
            response.set_cookie(key="lang", value=lang, max_age=31536000, httponly=False)

        response.headers["Content-Language"] = lang
        return response
