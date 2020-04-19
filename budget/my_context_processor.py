import django
from django.conf import settings
def cp(request):
    ctx = {
        "now": django.utils.timezone.now(),
        "version": "3.0"
    }
    return ctx

def recaptcha_site_key(request):
    return {'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY}