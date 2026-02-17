# enviar_pdf_respuestas.py
# Lee respuestas del Form, genera PDFs y los envía por email

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from leer_sheets import leer_respuestas_form, conectar_google_sheets
from generar_pdf_respuestas import generar_pdf_desde_respuesta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment
from sendgrid.helpers.mail import FileContent, FileName, FileType, Disposition
from dotenv import load_dotenv
import base64

load_dotenv('src/.env')

def enviar_pdf_por_email(email_destino, nombre_consultorio, ruta_pdf):
    """
    Envía el PDF de evidencia por email al consultorio
    """
    api_key = os.getenv('SENDGRID_API_KEY')
    email_remitente = 'jenniffercelisn@gmail.com'
    
    # Leer el archivo PDF
    with open(ruta_pdf, 'rb') as f:
        pdf_data = f.read()
    
    # Codificar en base64
    pdf_encoded = base64.b64encode(pdf_data).decode()
    
    # Crear el attachment
    attachment = Attachment(
        FileContent(pdf_encoded),
        FileName(os.path.basename(ruta_pdf)),
        FileType('application/pdf'),
        Disposition('attachment')
    )
    
    message = Mail(
        from_email=email_remitente,
        to_emails=email_destino,
        subject=f'✅ Tu Evidencia de Revisión - Alertas INVIMA',
        html_content=f'''
<div style="font-family: Arial, sans-serif; max-width: 600px;">
    <h2 style="color: #4CAF50;">✅ Evidencia Generada Exitosamente</h2>
    
    <p>Hola <strong>{nombre_consultorio}</strong>,</p>
    
    <p>Gracias por completar la revisión de alertas sanitarias.</p>
    
    <p>Adjunto encontrarás tu <strong>PDF de evidencia</strong> listo para:</p>
    <ul>
        <li>Archivar en tu consultorio</li>
        <li>Presentar en auditorías del INVIMA</li>
        <li>Documentar cumplimiento normativo</li>
    </ul>
    
    <p style="background: #e3f2fd; padding: 15px; border-left: 4px solid #2196F3;">
        💡 <strong>Tip:</strong> Guarda este PDF en tu carpeta de documentos legales.
    </p>
    
    <p>Si tienes alguna pregunta, responde a este email.</p>
    
    <p style="color: #666; font-size: 12px; margin-top: 30px;">
        Sistema Automatizado de Alertas Sanitarias INVIMA
    </p>
</div>
'''
    )
    
    message.attachment = attachment
    
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(f"✅ PDF enviado exitosamente a {email_destino}")
        return True
    except Exception as e:
        print(f"❌ Error al enviar PDF: {str(e)}")
        return False


def marcar_respuesta_procesada(fila_numero):
    """
    Marca una respuesta como procesada en el Google Sheet
    """
    client = conectar_google_sheets()
    sheet_id = '1GxIK0GZTeNHI4XmJme48qyidXUNKhvVqJJQFzyJNFmk'
    sheet = client.open_by_key(sheet_id).sheet1
    
    # La columna PDF_Enviado debería ser la última (columna 10)
    # Ajusta este número si agregaste la columna en otra posición
    columna_pdf_enviado = 10
    
    sheet.update_cell(fila_numero, columna_pdf_enviado, 'SI')
    print(f"✅ Respuesta {fila_numero} marcada como procesada")


def procesar_respuestas_pendientes():
    """
    Función principal que procesa todas las respuestas pendientes
    """
    print("=" * 50)
    print("🚀 PROCESANDO RESPUESTAS DEL FORM")
    print("=" * 50)
    
    # Leer todas las respuestas
    respuestas = leer_respuestas_form()
    
    if not respuestas:
        print("ℹ️  No hay respuestas en el Form todavía.")
        return
    
    # Filtrar solo las que no tienen PDF enviado
    respuestas_pendientes = []
    for i, respuesta in enumerate(respuestas, start=2):  # start=2 porque fila 1 es header
        pdf_enviado = respuesta.get('PDF_Enviado', '')
        if pdf_enviado != 'SI':
            respuestas_pendientes.append((i, respuesta))
    
    if not respuestas_pendientes:
        print("✅ Todas las respuestas ya fueron procesadas.")
        return
    
    print(f"\n📋 Respuestas pendientes: {len(respuestas_pendientes)}\n")
    
    # Procesar cada respuesta pendiente
    pdfs_enviados = 0
    pdfs_fallidos = 0
    
    for fila_numero, respuesta in respuestas_pendientes:
        nombre = respuesta.get('Nombre Completo del Consultorio', 'Sin nombre')
        email = respuesta.get('Email de contacto', '')
        
        print(f"{'='*50}")
        print(f"Procesando: {nombre}")
        print(f"{'='*50}")
        
        # Generar PDF
        print("1. Generando PDF...")
        ruta_pdf = generar_pdf_desde_respuesta(respuesta)
        
        # Enviar por email
        print("2. Enviando por email...")
        exito = enviar_pdf_por_email(email, nombre, ruta_pdf)
        
        if exito:
            # Marcar como procesada
            print("3. Marcando como procesada...")
            marcar_respuesta_procesada(fila_numero)
            pdfs_enviados += 1
        else:
            pdfs_fallidos += 1
        
        print()
    
    # Resumen final
    print("=" * 50)
    print("📊 RESUMEN")
    print("=" * 50)
    print(f"   PDFs enviados   : {pdfs_enviados}")
    print(f"   PDFs fallidos   : {pdfs_fallidos}")
    print("=" * 50)
    print("✅ Proceso completado")


if __name__ == "__main__":
    procesar_respuestas_pendientes()
    