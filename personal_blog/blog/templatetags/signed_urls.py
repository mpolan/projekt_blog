import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils.supabase_storage import get_signed_image_url

from django import template


register = template.Library()

@register.filter
def signed_url(path):
    return get_signed_image_url(path)
