🏥 Sistema de Alertas Sanitaria del Invima

MVP(Minimum Viable Product) de un sistema que automatiza la revision de alertas sanitarial del INVIMA semanalmente y generación de documento en PDF que valida su revisión.

📋 Contexto

Parte de la actividad de auditoria y habilitación en salud para todo consultorio particular, IPS y fabricantes deben revisar y registrar de forma periódica las alertas sanitarias emitidas por el INVIMA. Para el auditor o profesional puede ser dispendiosa esta labor. Este sistema permite liberar un poco la carga administrativa que representa.  

🎯 Objetivo del repositorio

Demostrar la construcción de una solución digital para automatizar el monitoreo y envío de alertas sanitarias del INVIMA a los actores implicados.

📁 Contenido

- main.py — Script principal. Lee las alertas nuevas del INVIMA, las envía por email a cada consultorio y las marca como enviadas en Google Sheets.
- enviar_notificacion.py — Gestiona el envío de emails con las alertas sanitarias usando SendGrid.
- enviar_pdf_respuestas.py — Lee las respuestas del Google Form, genera un PDF de evidencia por consultorio y lo envía por email.
generar_pdf_respuestas.py — Genera el PDF de evidencia de revisión a partir de las respuestas del formulario.
- leer_sheets.py — Maneja la conexión con Google Sheets y lee tanto las alertas como las respuestas del Form y los consultorios registrados.
- links_personalizados_forms.py — Genera links personalizados del Google Form con el nombre del consultorio pre-cargado automáticamente.
- requirements.txt — Librerías de Python necesarias para ejecutar el sistema.

💻 Tecnologías
* Python 3.x
* Jupyter Notebooks
* Librería json (nativa de Python)
  
👩‍⚕️ Autora

Jenniffer Celis Médica con 10 años de experiencia clínica, con apuesta al healthtech. Conocimientos en Python, SQL, análisis de datos y creación de soluciones digitales en salud.

* 🌐 Portfolio: jenniffer-celis.netlify.app
* 💼 LinkedIn: linkedin.com/in/jenniffer-celis
  
📚 Referencias

- Alertas Sanitarias INVIMA - Medicamentos y Productos Biológicos


