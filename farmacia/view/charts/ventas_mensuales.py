from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from datetime import datetime, timedelta
from ...models import Facturas

def api_ventas_mensuales(request):
    hoy = datetime.now()
    hace_un_año = hoy - timedelta(days=365)

    meses_nombre = {
        1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"
    }

    ventas = (
        Facturas.objects
        .filter(fecha__isnull=False, fecha__gte=hace_un_año)
        .annotate(mes=ExtractMonth('fecha'))
        .values('mes')
        .annotate(total=Count('facturaid'))
        .order_by('mes')
    )

    # Diccionario con ventas por mes
    totales_dict = {v['mes']: v['total'] for v in ventas}
    sales_labels = [meses_nombre[m] for m in range(1, 13)]
    sales_data = [totales_dict.get(m, 0) for m in range(1, 13)]

    return JsonResponse({
        'sales_labels': sales_labels,
        'sales_data': sales_data
    })
    

