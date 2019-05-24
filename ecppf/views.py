"""Vistas apliacion"""

from django.http import HttpResponse

from datetime import datetime

def hello_world(request):
    now = datetime.now().strftime('%b %dth, %Y - %H:%M Hrs')
    return HttpResponse('Hola Mundo - Hello World! - La Hora es {now}'.format(now=now))


def mensaje(request):
	return HttpResponse('mensaje.html')
