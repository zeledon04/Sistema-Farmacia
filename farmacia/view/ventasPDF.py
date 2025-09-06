from decimal import Decimal
import json
import pdfkit  # type: ignore
import base64
from django.http import HttpResponse , JsonResponse 
from django.conf import settings
from ..models import Usuarios  
from datetime import datetime

from ..utils import admin_required

@admin_required
def registro_ventas_pdf(request):
    pdf_file = "theme/registro_ventas.pdf"
    with open(pdf_file, 'rb') as f:
        pdf_data = f.read()
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="registro_ventas.pdf"'
    return response

def imprimir_registro_ventas(request):
    if request.method == 'POST':
        items_json = request.body.decode('utf-8')
        
        data = json.loads(items_json)
        datos = data['items']
        rutaLogo = settings.LOGO_PATH
        vendedor = Usuarios.objects.get(pk=request.session['user_id'])
        nombreVendedor = f"{vendedor.nombre}"

        generar_registro_facturas(datos, rutaLogo,nombreVendedor)

    return JsonResponse({'success': True})

def generar_registro_facturas(datos, ruta, nombreVendedor):
    def image_to_base64(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    logo_base64 = image_to_base64(ruta)

    fecha_actual = datetime.now()

    dias_semana = {
        'Monday': 'Lunes',
        'Tuesday': 'Martes',
        'Wednesday': 'Miércoles',
        'Thursday': 'Jueves',
        'Friday': 'Viernes',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }

    dia_semana = dias_semana[fecha_actual.strftime("%A")]
    fecha_formateada = f"{dia_semana} {fecha_actual.strftime('%d/%m/%Y %I:%M %p').lower()}"

    ticket_html = f"""
    <html>
    <head>
        <title>Historial de Ventas</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f9; border-radius: 10px;}}
            .center {{ text-align: center;}}
            #logo {{ width: 220px; height: auto; margin-bottom: 10px; padding-top: 20px; }}
            table {{ width: 90%; margin: 20px auto; border-collapse: collapse; box-shadow: 0 2px 3px rgba(0,0,0,0.1); border-radius: 7px; overflow: hidden; }}
            th, td {{ border: 1px solid #ddd; text-align: left; padding: 8px; font-size: 12px; }}
            th {{ background-color: #4CAF50; color: white; font-weight: bold; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            tr:hover {{ background-color: #f1f1f1; }}
            .footer {{ text-align: center; margin-top: 20px; }}
            .footer p {{ font-size: 14px; color: #333; }}
        </style>
    </head>
    <body>
        <div class="center">
            <img id="logo" src="data:image/png;base64,{logo_base64}" alt="Logo">
            <p style="margin-bottom: 1; margin-top: 10px; font-size: 14px; font-weight: bold;">FARMACIA SAGRADO CORAZÓN DE JESÚS</p>
            <p style="margin: 1; font-size: 10px;">{fecha_formateada}</p>
            <p>Historial de Ventas</p>
        </div>

        <table>
            <tr>
                <th class="p-2">#</th>
                <th class="p-2">Producto</th>
                <th class="p-2">Fecha</th>
                <th class="p-2">Cantidad</th>
                <th class="p-2">Precio Venta</th>
                <th class="p-2">SubtotalVenta</th>
                <th class="p-2">Precio Compra</th>
                <th class="p-2">SubtotalCompra</th>

            </tr>
    """
    totall = 0
    totalPrecioCompra = 0
    
    for data in datos:
        numero = data['numero']
        producto = data['producto']
        fecha = data['fecha']
        precioCompra = data['precioCompra']
        cantidad = data['cantidad']
        precioVenta = data['precioVenta']
        subtotal = Decimal(str(data['subtotal']))
        sub = Decimal(str(precioCompra)) * int(cantidad)
        
        ticket_html += f"""
            <tr>
                <td>{numero}</td>
                <td>{producto}</td>
                <td>{fecha}</td>
                <td>{cantidad}</td>
                <td>C$ {Decimal(precioVenta):.2f}</td>
                <td>C$ {subtotal:.2f}</td>
                <td>C$ {Decimal(precioCompra):.2f}</td>
                <td>C$ {sub:.2f}</td>
            </tr>
        """
        totall += subtotal
        totalPrecioCompra += sub

    ticket_html += f"""
            <tr style="background-color: #e2f0d9; font-weight: bold;">
                <td colspan="5">Total</td>
                <td>C$ {totall:.2f}</td>
                <td>----</td>
                <td>C$ {totalPrecioCompra:.2f}</td>
            </tr>
            <tr style="background-color: #d9edf7; font-weight: bold;">
                <td colspan="7">Ganancia</td>
                <td>C$ {(totall - totalPrecioCompra):.2f}</td>
            </tr>
            
        </table>
        <div class="footer">
            <p>Generado por: {nombreVendedor}</p>
        </div>
    </body>
    </html>
    """

    html_file = "theme/registroTempoVentas.html"
    with open(html_file, "w") as f:
        f.write(ticket_html)

    pdf_file = "theme/registro_ventas.pdf"
    config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)
    pdfkit.from_file(html_file, pdf_file, configuration=config)










