## Herramientas de Automatización en Python

Este directorio contiene scripts desarrollados en Python para automatizar tareas operativas y de evasión en simulaciones de seguridad.

### 1. DOM Smuggler v2 (`dom_smuggler_v2.py`)
Herramienta diseñada para simulaciones de *Red Teaming* y auditorías de seguridad (Phishing/Ingeniería Social). Utiliza técnicas de **HTML Smuggling** para evadir sistemas de detección de intrusos (IDS) y sandboxes de correo.

* **Funcionamiento:** Toma una plantilla HTML de entrada, fuerza los métodos POST para la captura de credenciales y ofusca el código fuente dividiéndolo en fragmentos codificados en Base64.
* **Evasión (Anti-Sandbox):** El payload decodifica y reconstruye el DOM del navegador (renderizando la página real) únicamente tras detectar interacción humana (`mousemove` o `touchstart`), evadiendo así los análisis automatizados que no interactúan con la página.
* **Uso:** ```bash
    python dom_smuggler_v2.py <plantilla_original.html> <payload_ofuscado.html>
    ```

### 2. Generador de QR para CV (`qr_cv_generator.py`)
Script utilitario para generar de forma automatizada códigos QR apuntando a recursos web (por defecto, el portafolio personal).

* **Funcionamiento:** Utiliza la librería `qrcode` para generar una imagen `.png` a partir de una URL especificada.
* **Gestión de archivos:** Verifica la existencia de un directorio de salida (`QRs_Generados`) y lo crea automáticamente si no existe antes de guardar la imagen.
* **Uso:** Simplemente ejecutar el script. Las variables de configuración (`URL_A_CODIFICAR`, `NOMBRE_ARCHIVO`) se pueden modificar directamente en la cabecera del archivo.
    ```bash
    python qr_cv_generator.py
    ```
