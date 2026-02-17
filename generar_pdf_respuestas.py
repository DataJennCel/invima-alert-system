from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generar_pdf_desde_respuesta(respuesta):
    """
    Genera un PDF de evidencia desde una respuesta del Google Form
    """
    # Extraer datos básicos
    nombre_consultorio = respuesta.get('Nombre Completo del Consultorio', 'Sin nombre')
    email = respuesta.get('Email de contacto', 'Sin email')
    timestamp = respuesta.get('Timestamp', datetime.now().strftime('%d/%m/%Y %H:%M'))
    
    # Separar alertas que APLICAN vs NO APLICAN
    alertas_aplican = []
    alertas_no_aplican = []
    
    print("🔍 Analizando respuestas...")
    
    for columna, valor in respuesta.items():
        # Buscar columnas que empiecen con "Por favor indica"
        if columna.startswith('Por favor indica'):
            # Extraer el título de la alerta entre [[...]]
            inicio = columna.find('[[')
            fin = columna.rfind(']')
            
            if inicio != -1 and fin != -1:
                titulo_alerta = columna[inicio+2:fin]  # Extraer [001] Medicamento...
                
                print(f"  Alerta: {titulo_alerta[:50]}...")
                print(f"  Respuesta: '{valor}'")
                
                if valor == 'Aplica':
                    alertas_aplican.append(titulo_alerta)
                    print(f"    ✅ Agregada a APLICAN")
                elif valor == 'No aplica':
                    alertas_no_aplican.append(titulo_alerta)
                    print(f"    ❌ Agregada a NO APLICAN")
                else:
                    print(f"    ⚠️ Valor desconocido: '{valor}'")
    
    print(f"\n📊 Resumen:")
    print(f"  APLICAN: {len(alertas_aplican)}")
    print(f"  NO APLICAN: {len(alertas_no_aplican)}\n")
    
    # Crear nombre del archivo
    fecha_archivo = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"evidencia_{nombre_consultorio.replace(' ', '_')}_{fecha_archivo}.pdf"
    ruta_completa = f"output/{nombre_archivo}"
    
    # Crear el PDF
    c = canvas.Canvas(ruta_completa, pagesize=letter)
    width, height = letter
    
    # TÍTULO
    c.setFont("Helvetica-Bold", 18)
    c.drawString(100, height - 80, "EVIDENCIA DE REVISIÓN")
    c.drawString(100, height - 105, "ALERTAS SANITARIAS INVIMA")
    
    # INFORMACIÓN DEL CONSULTORIO
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 140, "Consultorio:")
    c.setFont("Helvetica", 12)
    c.drawString(210, height - 140, nombre_consultorio)
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 160, "Email:")
    c.setFont("Helvetica", 12)
    c.drawString(210, height - 160, email)
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 180, "Fecha de revisión:")
    c.setFont("Helvetica", 12)
    c.drawString(210, height - 180, timestamp)
    
    # LÍNEA SEPARADORA
    c.line(100, height - 200, 500, height - 200)
    
    y_position = height - 230
    
    # ALERTAS QUE APLICAN
    c.setFont("Helvetica-Bold", 14)
    c.setFillColorRGB(0, 0.5, 0)  # Verde
    c.drawString(100, y_position, f"✅ ALERTAS QUE APLICAN ({len(alertas_aplican)})")
    c.setFillColorRGB(0, 0, 0)  # Negro
    y_position -= 25
    
    if alertas_aplican:
        c.setFont("Helvetica", 10)
        for alerta in alertas_aplican:
            # Dividir si es muy largo
            if len(alerta) > 70:
                linea1 = alerta[:70]
                linea2 = alerta[70:140]
                c.drawString(120, y_position, f"• {linea1}")
                y_position -= 12
                if linea2:
                    c.drawString(130, y_position, linea2)
                    y_position -= 15
            else:
                c.drawString(120, y_position, f"• {alerta}")
                y_position -= 15
    else:
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(120, y_position, "Ninguna alerta aplica a este consultorio")
        y_position -= 15
    
    y_position -= 20
    
    # ALERTAS QUE NO APLICAN
    c.setFont("Helvetica-Bold", 14)
    c.setFillColorRGB(0.7, 0, 0)  # Rojo
    c.drawString(100, y_position, f"❌ ALERTAS QUE NO APLICAN ({len(alertas_no_aplican)})")
    c.setFillColorRGB(0, 0, 0)  # Negro
    y_position -= 25
    
    if alertas_no_aplican:
        c.setFont("Helvetica", 10)
        for alerta in alertas_no_aplican:
            if len(alerta) > 70:
                linea1 = alerta[:70]
                linea2 = alerta[70:140]
                c.drawString(120, y_position, f"• {linea1}")
                y_position -= 12
                if linea2:
                    c.drawString(130, y_position, linea2)
                    y_position -= 15
            else:
                c.drawString(120, y_position, f"• {alerta}")
                y_position -= 15
    else:
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(120, y_position, "Todas las alertas aplican a este consultorio")
        y_position -= 15
    
    # SECCIÓN DE FIRMA
    y_position -= 40
    c.line(100, y_position, 500, y_position)
    y_position -= 30
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(100, y_position, "Revisado por:")
    c.line(200, y_position - 5, 450, y_position - 5)
    
    y_position -= 30
    c.drawString(100, y_position, "Firma:")
    c.line(200, y_position - 5, 450, y_position - 5)
    
    y_position -= 40
    c.setFont("Helvetica", 8)
    c.drawString(100, y_position, f"Documento generado automáticamente el {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    c.drawString(100, y_position - 12, "Sistema de Alertas Sanitarias INVIMA")
    
    # Guardar
    c.save()
    
    print(f"✅ PDF generado: {ruta_completa}")
    return ruta_completa


# CÓDIGO DE PRUEBA
if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from leer_sheets import leer_respuestas_form
    
    print("🧪 Probando generación de PDF desde respuestas...\n")
    
    respuestas = leer_respuestas_form()
    
    if respuestas:
        print(f"Se encontraron {len(respuestas)} respuestas\n")
        for i, respuesta in enumerate(respuestas, 1):
            print(f"{'='*50}")
            print(f"Procesando respuesta {i}...")
            print(f"{'='*50}")
            generar_pdf_desde_respuesta(respuesta)
            print()
    else:
        print("No hay respuestas todavía en el Form")