from django.conf import settings

def csf(request):
    return {
        'DEBUG': settings.DEBUG,
        }
    
