from django.conf import settings


def global_settings(request):
    return {
        'PRIMARY_COLOR': '#003366',
        'SECONDARY_COLOR': '#FF6600'
    }