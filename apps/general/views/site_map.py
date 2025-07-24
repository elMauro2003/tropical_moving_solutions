from django.http import HttpResponse
from django.conf import settings
from django.template.loader import render_to_string

def sitemap(request):
    """Sitemap txt"""
    # Remove empty lines
    text_with_empty_lines = render_to_string(
        "txts/sitemap.txt",
        {
            "domain": settings.DOMAIN_URL,
        },
    )
    text_without_empty_lines = "\n".join([line.strip() for line in text_with_empty_lines.splitlines() if line.strip()])
    # Render sitemap txt
    return HttpResponse(text_without_empty_lines, content_type="text/plain")