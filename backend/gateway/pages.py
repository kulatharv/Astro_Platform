"""HTML Page Routes for Gateway App."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from shared.i18n.translation import load_translations

router = APIRouter(tags=["Pages"])


def _render_page(request: Request, template_name: str, context: dict | None = None) -> HTMLResponse:
    templates = request.app.state.templates
    lang = request.cookies.get("lang", "en")
    page_context = {"request": request, "lang": lang, "t": load_translations(lang)}
    if context:
        page_context.update(context)
    return templates.TemplateResponse(template_name, page_context)


@router.get("/", response_class=HTMLResponse)
@router.get("/{lang}/", response_class=HTMLResponse)
def home_page(request: Request, lang: str = "en"):
    return _render_page(request, "index.html")


@router.get("/prediction", response_class=HTMLResponse)
@router.get("/{lang}/prediction", response_class=HTMLResponse)
def prediction_html_page(request: Request, lang: str = "en"):
    return _render_page(request, "prediction.html")


@router.get("/chat", response_class=HTMLResponse)
@router.get("/{lang}/chat", response_class=HTMLResponse)
def chat_html_page(request: Request, lang: str = "en"):
    return _render_page(request, "chat.html")


@router.get("/panchang.html", response_class=HTMLResponse)
@router.get("/panchang", response_class=HTMLResponse)
@router.get("/{lang}/panchang", response_class=HTMLResponse)
def panchang_html_page(request: Request, lang: str = "en"):
    return _render_page(request, "panchang.html")


@router.get("/blogs", response_class=HTMLResponse)
@router.get("/{lang}/blogs", response_class=HTMLResponse)
def blogs_html_page(request: Request, lang: str = "en"):
    return _render_page(request, "blogs.html")


@router.get("/about", response_class=HTMLResponse)
@router.get("/{lang}/about", response_class=HTMLResponse)
def about_html_page(request: Request, lang: str = "en"):
    return _render_page(request, "about.html")


@router.get("/horoscope", response_class=HTMLResponse)
@router.get("/{lang}/horoscope", response_class=HTMLResponse)
def horoscope_html_page(request: Request, lang: str = "en"):
    return _render_page(request, "daily-horoscope.html")


@router.get("/kundali", response_class=HTMLResponse)
@router.get("/{lang}/kundali", response_class=HTMLResponse)
def kundali_html_page(request: Request, lang: str = "en"):
    return _render_page(request, "kundali.html")


@router.get("/blog/{blog_id}", response_class=HTMLResponse)
def blog_detail_html_page(request: Request, blog_id: int):
    return _render_page(request, "blog-detail.html", {"blog_id": blog_id})


@router.get("/admin/login", response_class=HTMLResponse)
def admin_login_html_page(request: Request):
    return _render_page(request, "admin-login.html")


@router.get("/admin/blogs", response_class=HTMLResponse)
def admin_blogs_html_page(request: Request):
    return _render_page(request, "admin-blog.html")
