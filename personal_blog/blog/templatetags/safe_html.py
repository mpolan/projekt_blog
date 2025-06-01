from django import template
from django.utils.safestring import mark_safe
import bleach

register = template.Library()

@register.filter(name='render_html')
def render_html(value):
    # Filtrowanie HTML, pozwalając tylko na bezpieczne tagi i atrybuty
    allowed_tags = ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'a', 'blockquote', 'code', 'pre', 'img', 'h1', 'h2', 'h3']
    allowed_attributes = {
        'a': ['href', 'title', 'rel'],
        'img': ['src', 'alt'],
    }
    cleaned_html = bleach.clean(value, tags=allowed_tags, attributes=allowed_attributes, strip=True)
    return mark_safe(cleaned_html)
