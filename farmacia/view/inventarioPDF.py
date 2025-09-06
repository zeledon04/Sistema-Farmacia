import pdfkit  # type: ignore
import base64
from django.http import HttpResponse 
from django.conf import settings
from ..models import Usuarios, Productos  
from datetime import datetime

def imprimir_registro_inventario(request):
    datos = Productos.objects.filter(estado=1)
    
    rutaLogo = settings.LOGO_PATH
    vendedor = Usuarios.objects.get(pk=request.session['user_id'])
    nombreVendedor = f"{vendedor.nombre}"

    # Generar el PDF
    generar_registro_inventario(datos, rutaLogo,nombreVendedor)
    
    # Ruta del PDF generado
    pdf_file = "theme/registro_inventario.pdf"
    with open(pdf_file, 'rb') as f:
        pdf_data = f.read()
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="registro_inventario.pdf"'
    return response

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
        'Sunday': 'Domingo'
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
        print(data.nombre)
        numero = count
        producto = data.nombre
        cantidad = data.stock
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
    
    html_file = "theme/registroTempoInventario.html"
    with open(html_file, "w") as f:
        f.write(ticket_html)

    pdf_file = "theme/registro_inventario.pdf"
    config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)
    pdfkit.from_file(html_file, pdf_file, configuration=config)





