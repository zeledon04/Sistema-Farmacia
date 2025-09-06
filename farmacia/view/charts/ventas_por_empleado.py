# views.py
from django.db.models import Sum
from django.http import JsonResponse
from ...models import Detallefacturas
from django.db.models import Count

def ventas_por_empleado(request):
    data = (
        Detallefacturas.objects
        .filter(facturaid__estado=1)
        .values('facturaid__usuarioid__nombre') # se accede a través de foreign key hasta el nombre del usuario.
        .annotate(total=Count('facturaid'))
        .order_by('-total')
    )

    labels = []
    totals = []

    for registro in data:
        labels.append(registro['facturaid__usuarioid__nombre'])
        totals.append(registro['total'])

    return JsonResponse({
        'labels': labels,
        'data': totals
    })
