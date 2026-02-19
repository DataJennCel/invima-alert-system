
def generar_link_personalizado(nombre_consultorio): #Genera un link personalizado del Google Form con el nombre pre-llenado. Parámetros: nombre_consultorio: Nombre del consultorio (ej: "Consultorio Dr Juan Perez"). Retorna: URL completa del formulario con el nombre pre-cargado
    
    # Tu link base del Form
    link_base = "https://docs.google.com/forms/d/e/1FAIpQLSeuZaoRuwXJynpzeUVw3s9p9XaJWV4k87nRcK-CsYBY5hU17Q/viewform?usp=header"
    
    # ID del campo "Nombre Completo del Consultorio"
    entry_id = "1917722040"
    
    # Reemplazar espacios por +
    nombre_encoded = nombre_consultorio.replace(" ", "+")
    
    # Construir URL completa
    link_completo = f"{link_base}?usp=pp_url&entry.{entry_id}={nombre_encoded}"
    
    return link_completo


# PRUEBA
if __name__ == "__main__":
    # Lista de consultorios de prueba
    consultorios = [
        "Consultorio Dr Juan Perez",
        "Consultorio Dental Sonrisa",
        "Consultorio Estetica Bella"
    ]
    
    print("🔗 LINKS PERSONALIZADOS GENERADOS:\n")
    
    for consultorio in consultorios:
        link = generar_link_personalizado(consultorio)
        print(f"📍 {consultorio}")
        print(f"   {link}\n")

## 🧪 **PRUEBA QUE FUNCIONA:**
#1. **Copia este link** (es para "Dr Juan Perez"):
# https://docs.google.com/forms/d/e/1FAIpQLSfYXifeB1aPVOS6RQNjiWmU6lMJHaddR9wdLUnhX51X0XLIHg/viewform?usp=pp_url&entry.1917722040=Consultorio+Dr+Juan+Perez
