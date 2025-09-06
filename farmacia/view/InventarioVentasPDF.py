import json
import pdfkit  # type: ignore
import base64
from django.http import HttpResponse , JsonResponse 
from django.conf import settings
import os
from django.db import models

from ..models import Detallefacturas, Usuarios  
from datetime import datetime


def registro_inventario_pdf(request):
    temp_dir = os.path.join(os.environ.get('LOCALAPPDATA'), 'Farmacia', 'tmp')
    pdf_file = os.path.join(temp_dir, 'registro_inventario.pdf')
    with open(pdf_file, 'rb') as f:
        pdf_data = f.read()
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="registro_inventario.pdf"'
    return response

def inventario_pdf(request):
    if request.method == 'POST':
        items_json = request.body.decode('utf-8')
        
        data = json.loads(items_json)
        
        
        fecha_obj = datetime.strptime(data['fecha'], "%d/%m/%Y %I:%M %p").date()
        rutaLogo = settings.LOGO_PATH
        vendedor = Usuarios.objects.get(pk=request.session['user_id'])
        nombreVendedor = f"{vendedor.nombre}"


        datos = (
            Detallefacturas.objects
            .filter(facturaid__fecha__date=fecha_obj, estado=1)
            .values(
                nombre_producto=models.F("productoid__nombre"),
                stock_actual=models.F("productoid__stock")
            )
            .distinct()
            .order_by("productoid__nombre")
        )

        print(datos)
        
        
        generar_registro_inventario(datos, rutaLogo, nombreVendedor)
        
    return JsonResponse({'success': True})


def generar_registro_inventario(datos, ruta, nombreVendedor):
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
        'Sunday': 'Domingo',
    }
    dia_semana = dias_semana[fecha_actual.strftime("%A")]
    fecha_formateada = f"{dia_semana} {fecha_actual.strftime('%d/%m/%Y %I:%M %p').lower()}"
    
    ticket_html = f"""
    <html>
    <head>
        <title>Inventario</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f9; border-radius: 10px;}}
            .center {{ text-align: center;}}
            #logo {{ width: 220px; height: auto; margin-bottom: 10px; padding-top: 20px; }}
            table {{ width: 90%; margin: 20px auto; border-collapse: collapse; box-shadow: 0 2px 3px rgba(0,0,0,0.1); border-radius: 7px; overflow: hidden; }}
            th, td {{ border: 1px solid #ddd; text-align: center; padding: 8px; font-size: 12px; }}
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
            <p>Inventario</p>
        </div>

        <table>
            <tr>
                <th class="p-2">#</th>
                <th class="p-2">Producto</th>
                <th class="p-2">Cantidad</th>
            </tr>
    """
    count = 1
    for data in datos:
        numero = count
        producto = data['nombre_producto']
        cantidad = data['stock_actual']
        # cantidad = 4
        count+=1
        
        ticket_html += f"""
            <tr>
                <td>{numero}</td>
                <td>{producto}</td>
                <td>{cantidad}</td>
            </tr>
        """

    ticket_html += f"""
        </table>
        <div class="footer">
            <p>Generado por: {nombreVendedor}</p>
        </div>
    </body>
    </html>
    """

    temp_dir = os.path.join(os.environ.get('LOCALAPPDATA'), 'Farmacia', 'tmp')
    os.makedirs(temp_dir, exist_ok=True)
    html_file = os.path.join(temp_dir, 'registroTempoInventario.html')
    pdf_file = os.path.join(temp_dir, 'registro_inventario.pdf')
    
    with open(html_file, "w") as f:
        f.write(ticket_html)
        
    config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)
    pdfkit.from_file(html_file, pdf_file, configuration=config)