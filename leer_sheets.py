
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os  # Carga las credenciales desde el archivo JSON


def conectar_google_sheets():
    """
    Conecta con Google Sheets usando las credenciales del service account
    
    Retorna:
    - client: Cliente autenticado de gspread
    """
    # Define el alcance (scope) de acceso
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    
    # Al inicio del archivo, después de los imports
    ruta_credentials = os.path.join(os.path.dirname(__file__), 'google-credentials.json')

    # Dentro de la función conectar_google_sheets:
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
    ruta_credentials,
    scope
)
    
    # Autoriza y crea el cliente
    client = gspread.authorize(credentials)
    
    print("✅ Conexión exitosa con Google Sheets")
    return client


def leer_consultorios():
    """
    Lee la lista de consultorios desde Google Sheets
    
    Retorna:
    - Lista de diccionarios con datos de cada consultorio
    """
    # Conectar
    client = conectar_google_sheets()
    
    # Abrir el Sheet por su ID (de la URL)
    sheet_id = '10XhdmKbmbC5m92G0WM-9oblhPdJlB48_GhQzrJ3ne-o'
    sheet = client.open_by_key(sheet_id).sheet1  # Primera hoja
    
    # Obtener todos los registros como lista de diccionarios
    consultorios = sheet.get_all_records()
    
    print(f"✅ Se encontraron {len(consultorios)} consultorios")
    
    return consultorios


def leer_alertas():
    """
    Lee las alertas de la semana desde Google Sheets
    
    Retorna:
    - Lista de diccionarios con datos de cada alerta
    """
   
    client = conectar_google_sheets()  # Conectar
    sheet_id = '116tVNtLb9uzb_811YJ8I54Cvf-ovA0NfnqwXPhQfHHE'  # Abrir el Sheet de alertas
    sheet = client.open_by_key(sheet_id).sheet1
    alertas = sheet.get_all_records()  # Obtener todas las alertas
    
    # Filtrar solo las que tienen estado "nueva"
    alertas_nuevas = [
        a for a in alertas 
        if a.get('Estado', '').strip().lower() == 'nueva'
    ] 
    
    print(f"✅ Se encontraron {len(alertas_nuevas)} alertas nuevas")
    
    return alertas_nuevas


def leer_respuestas_form():
    """
    Lee las respuestas del Google Form desde Google Sheets
    
    Retorna:
    - Lista de diccionarios con las respuestas
    """
    # Conectar
    client = conectar_google_sheets()
    
    # Abrir el Sheet de respuestas
    sheet_id = '12DveY-Czc_PcpvpvaoySMJkdwQ8HnqFSfU1TMpQz9ig'
    sheet = client.open_by_key(sheet_id).sheet1
    
    # Obtener todas las respuestas
    respuestas = sheet.get_all_records()
    
    print(f"✅ Se encontraron {len(respuestas)} respuestas")
    
    return respuestas


# CÓDIGO DE PRUEBA
if __name__ == "__main__":
    print("🧪 Probando conexión con Google Sheets...\n")
    
    # Prueba 1: Leer consultorios
    print("📋 CONSULTORIOS:")
    consultorios = leer_consultorios()
    # Primero ver qué columnas tiene
    if len(consultorios) > 0:
        print(f"  Columnas disponibles: {list(consultorios[0].keys())}\n")

    for c in consultorios:
        print(f"  - {c}")
    
    print("\n" + "="*50 + "\n")
    
    # Prueba 2: Leer alertas
    print("🚨 ALERTAS NUEVAS:")
    alertas = leer_alertas()
    for a in alertas:
        print(f"  - [{a['ID']}] {a['Titulo']}")
    
    print("\n" + "="*50 + "\n")
    
    # Prueba 3: Leer respuestas del form
    print("📝 RESPUESTAS DEL FORM:")
    respuestas = leer_respuestas_form()
    if len(respuestas) > 0:
        for r in respuestas:
            print(f"  - {r}")
    else:
        print("  (Aún no hay respuestas)")
