import django
def cp(request):
    ctx = {
        "now": django.utils.timezone.now(),
        "version": "2.0"
    }
    return ctx
