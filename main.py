# main.py
# Script principal que conecta todo el sistema INVIMA

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from leer_sheets import leer_alertas, leer_consultorios, conectar_google_sheets
from enviar_notificacion import enviar_alerta
from links_personalizados_forms import generar_link_personalizado

def marcar_alertas_enviadas():
    client = conectar_google_sheets()
    sheet_id = '116tVNtLb9uzb_811YJ8I54Cvf-ovA0NfnqwXPhQfHHE'
    sheet = client.open_by_key(sheet_id).sheet1
    datos = sheet.get_all_records()
    alertas_actualizadas = 0
    for i, fila in enumerate(datos, start=2):
        if fila.get('Estado', '').strip().lower() == 'nueva':
            sheet.update_cell(i, 6, 'enviada')
            alertas_actualizadas += 1
    print(f"✅ {alertas_actualizadas} alertas marcadas como 'enviada'")

def ejecutar_sistema():
    print("=" * 50)
    print("🚀 INICIANDO SISTEMA INVIMA")
    print("=" * 50)

    print("\n📋 PASO 1: Leyendo alertas nuevas...")
    alertas = leer_alertas()
    
    if not alertas:
        print("ℹ️  No hay alertas nuevas para procesar. Fin.")
        return
    
    # Ahora pasamos título Y link de cada alerta
    alertas_con_links = [
        {'titulo': a['Titulo'], 'link': a.get('Link_INVIMA', '')}
        for a in alertas
    ]
    print(f"   Alertas encontradas: {len(alertas_con_links)}")

    print("\n🏥 PASO 2: Leyendo consultorios...")
    consultorios = leer_consultorios()
    print(f"   Consultorios encontrados: {len(consultorios)}")

    print("\n📧 PASO 3: Enviando emails...")
    emails_enviados = 0
    emails_fallidos = 0

    for consultorio in consultorios:
        nombre = consultorio['Nombre_Consultorio']
        email  = consultorio['Email']
        link = generar_link_personalizado(nombre)
        print(f"\n   → Enviando a: {nombre} ({email})")
        exito = enviar_alerta(email, alertas_con_links, nombre, link)
        if exito:
            emails_enviados += 1
        else:
            emails_fallidos += 1

    print("\n✏️  PASO 4: Marcando alertas como enviadas en Google Sheets...")
    marcar_alertas_enviadas()

    print("\n" + "=" * 50)
    print("📊 RESUMEN")
    print("=" * 50)
    print(f"   Alertas procesadas : {len(alertas_con_links)}")
    print(f"   Emails enviados    : {emails_enviados}")
    print(f"   Emails fallidos    : {emails_fallidos}")
    print("=" * 50)
    print("✅ Sistema ejecutado exitosamente")

if __name__ == "__main__":
    ejecutar_sistema()