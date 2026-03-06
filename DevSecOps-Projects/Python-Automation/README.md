# Herramientas de Automatización en Python

Este directorio contiene scripts desarrollados en Python para automatizar tareas operativas y utilidades de uso diario.

### 1. Acortador de URLs Múltiple (`URL-Shortener-Tool.py`)

Script de automatización para acortar enlaces de manera rápida utilizando las APIs públicas de TinyURL y is.gd.

* **Funcionamiento:** Solicita al usuario una URL larga por consola y realiza peticiones HTTP (`GET`) a los endpoints de los acortadores. Maneja tiempos de espera (timeouts), errores de conexión y valida los códigos de estado de respuesta.
* **Uso:** ```bash
  python URL-Shortener-Tool.py
  ```

### 2. Generador de QR para CV (`qr_cv_generator.py`)

Script utilitario para generar de forma automatizada códigos QR apuntando a recursos web (por defecto, el portafolio o CV personal).

* **Funcionamiento:** Utiliza la librería `qrcode` para generar una imagen `.png` a partir de una URL especificada.
* **Gestión de archivos:** Verifica la existencia de un directorio de salida (`QRs_Generados`) y lo crea automáticamente si no existe antes de guardar la imagen.
* **Uso:** Simplemente ejecutar el script. Las variables de configuración (`URL_A_CODIFICAR`, `NOMBRE_ARCHIVO`) se pueden modificar directamente en la cabecera del archivo.
  ```bash
  python qr_cv_generator.py
  ```

### 3. Clonador y Consolidador de Plantillas HTML (`html_template_cloner.py`)

Script utilitario orientado a Red Teaming diseñado para clonar sitios web objetivo y consolidar todos sus recursos externos (CSS y JavaScript) en un único archivo HTML estático. Ideal para generar *Landing Pages* para campañas de ingeniería social (ej. Gophish) o respaldos offline.

* **Funcionamiento:** Utiliza `requests` y `BeautifulSoup4` para descargar el DOM. Busca etiquetas `<link rel="stylesheet">` y `<script src="...">`, descarga su contenido y lo inyecta directamente (inlining) dentro de etiquetas `<style>` y `<script>` en el mismo archivo.
* **OPSEC / Evasión:** Incorpora cabeceras (User-Agent real), deshabilita advertencias SSL (`urllib3`) para operar en laboratorios autofirmados y elimina comentarios HTML originales para reducir la huella de detección.
* **Uso:** Al ejecutar, pedirá el dominio objetivo por consola.
  ```bash
  python html_template_cloner.py
  ```
