import django
def cp(request):
    ctx = {
        "now": django.utils.timezone.now(),
        "version": "3.0"
    }
    return ctx
