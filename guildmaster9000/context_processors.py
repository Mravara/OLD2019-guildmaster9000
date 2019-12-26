from django.conf import settings


def global_settings(request):
    return {
        'date_format': 'd-m-Y - H:i:s',
    }