from django.http import JsonResponse
from django.db.models.functions import ExtractMonth
from datetime import datetime, timedelta
from django.db.models import Sum, F, ExpressionWrapper, FloatField
from ...models import Detallefacturas

def api_ingresos_mensuales(request):
    hoy = datetime.now()
    hace_un_año = hoy - timedelta(days=365)

    meses_nombre = {
        1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"
    }

    ingresos = (
        Detallefacturas.objects
        .filter(facturaid__fecha__isnull=False, facturaid__fecha__gte=hace_un_año)
        .annotate(
            mes=ExtractMonth('facturaid__fecha'),
            ingreso=ExpressionWrapper(F('cantidad') * F('precio'), output_field=FloatField())
        )
        .values('mes')
        .annotate(total=Sum('ingreso'))
        .order_by('mes')
    )

    ingresos_dict = {v['mes']: round(v['total'], 2) for v in ingresos}
    sales_labels = [meses_nombre[m] for m in range(1, 13)]
    sales_data = [ingresos_dict.get(m, 0) for m in range(1, 13)]

    return JsonResponse({
        'sales_labels': sales_labels,
        'sales_data': sales_data
    })
