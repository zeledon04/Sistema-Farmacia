from django.http import JsonResponse
from ...models import Productos
from django.db.models import Count, Q

def estado_inventario(request):
    en_stock = Productos.objects.filter(stock__gt=30).count()
    bajo_stock = Productos.objects.filter(stock__gt=0, stock__lte=30).count()
    agotado = Productos.objects.filter(stock=0).count()

    return JsonResponse({
        'labels': ['En Stock', 'Bajo Stock', 'Agotado'],
        'data': [en_stock, bajo_stock, agotado]
    })
