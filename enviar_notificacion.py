import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv('src/.env')

def enviar_alerta(email_destino, alertas, nombre_consultorio, link_form):
    # alertas es ahora una lista de diccionarios: [{'titulo': '...', 'link': '...'}]
    api_key = os.getenv('SENDGRID_API_KEY')
    email_remitente = 'jenniffercelisn@gmail.com'

    # Construir lista HTML con título + link de cada alerta
    lista_alertas_html = ""
    for alerta in alertas:
        titulo = alerta['titulo']
        link   = alerta['link']
        lista_alertas_html += f"""
        <li style='margin-bottom: 15px;'>
            {titulo}<br>
            <a href='{link}' 
               style='color: #1565C0; font-size: 12px;'>
               🔗 Ver alerta completa en INVIMA
            </a>
        </li>
        """

    message = Mail(
        from_email=email_remitente,
        to_emails=email_destino,
        subject=f'🚨 Nuevas Alertas Sanitarias INVIMA - {nombre_consultorio}',
        html_content=f'''
<div style="font-family: Arial, sans-serif; max-width: 600px;">
    <h2 style="color: #d32f2f;">🚨 Nuevas Alertas Sanitarias INVIMA</h2>
    
    <p>Hola <strong>{nombre_consultorio}</strong>,</p>
    
    <p>Esta semana se publicaron <strong>{len(alertas)} nuevas alertas sanitarias</strong>.</p>
    
    <div style="background: #fff3cd; padding: 20px; margin: 20px 0; border-left: 4px solid #ffc107;">
        <h3>📋 Alertas de esta semana:</h3>
        <p style="font-size: 13px; color: #555;">
            Revisa cada alerta antes de completar el formulario.
        </p>
        <ul>
            {lista_alertas_html}
        </ul>
    </div>
    
    <div style="text-align: center; margin: 30px 0;">
        <a href="{link_form}" 
           style="background: #1565C0; color: white; padding: 15px 40px; 
                  text-decoration: none; font-size: 18px; border-radius: 5px; 
                  display: inline-block;">
            📄 GENERAR MI EVIDENCIA PDF
        </a>
    </div>
    
    <p><strong>⏰ Por favor completa el formulario antes del viernes.</strong><br>
    Recibirás tu PDF de evidencia automáticamente.</p>
    
    <p style="color: #666; font-size: 12px; margin-top: 30px;">
        Tu nombre ya está pre-cargado en el formulario. 
        Solo marca si cada alerta aplica o no a tu consultorio.
    </p>
</div>
'''
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(f"✅ Email enviado exitosamente a {email_destino}")
        print(f"   Código de respuesta: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Error al enviar email: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Ejecutando prueba de envío de email...\n")
    alertas_test = [
        {'titulo': 'ALERTA 001 - Medicamento PERJETA® falsificado', 'link': 'https://app.invima.gov.co'},
        {'titulo': 'ALERTA 002 - Termómetro digital no conforme', 'link': 'https://app.invima.gov.co'}
    ]
    link_prueba = "https://docs.google.com/forms/d/e/1FAIpQLSfYXifeB1aPVOS6RQNjiWmU6lMJHaddR9wdLUnhX51X0XLIHg/viewform?usp=pp_url&entry.1917722040=Consultorio+Demo"
    enviar_alerta("jenniffercelisn@gmail.com", alertas_test, "Consultorio Demo", link_prueba)