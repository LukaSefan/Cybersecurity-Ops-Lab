# Título del Escenario: Simulación de Kill Chain Completo: XSS Reflejado + Ingeniería Social Avanzada



## 🎯 Objetivo de la Prueba

Demostrar el impacto crítico de una vulnerabilidad de **Cross-Site Scripting (XSS)** no mitigada y cómo puede ser utilizada para encadenar ataques de suplantación de identidad (Phishing) con alta credibilidad.



* **Target:** Plataforma de E-Commerce Minorista (Anonimizado: "Retailer-X").



---



## ⛓️ Flujo Técnico de la Auditoría (Kill Chain)



### 1. Reconocimiento (Discovery)

Se identificó que el motor de búsqueda interno del sitio legítimo (`/catalogsearch/result`) no implementaba sanitización de entrada (*Input Sanitization*) en el parámetro `q`. Esto permitió la inyección de código JavaScript arbitrario (**Reflected XSS**).



### 2. Armado del Vector (Weaponization)

Se construyó una "URL Trampa" utilizando el dominio legítimo de la víctima para evadir filtros de concienciación de seguridad.



* **Técnica:** El enlace comienza con el dominio oficial (`retailer-x.com`), generando confianza inmediata en el usuario.

* **Payload:** Se inyectó un script de redirección (`window.location`) ofuscado que envía al usuario a un entorno controlado inmediatamente después de cargar la página legítima.



### 3. Infraestructura de Simulación (Infrastructure)

* **Dominio:** Se configuró un dominio mediante *Typosquatting* (similar al original) para mantener la persistencia visual.

* **Clonación:** Se replicó la interfaz gráfica del sitio (Login/Checkout) utilizando herramientas de clonación web para un escenario de "Pixel Perfect".

* **Backend:** Se desplegó un servidor VPS (Nginx + PHP) configurado únicamente para registrar eventos de ingreso de datos (Logs de Auditoría) sin procesar transacciones reales.



### 4. Ejecución y Explotación (Delivery & Actions)

1.  El usuario accede al enlace que parece legítimo.

2.  El sitio vulnerable ejecuta el XSS y redirige al usuario al entorno clonado de forma transparente.

3.  El usuario interactúa con el formulario simulado.

4.  El sistema captura los metadatos de la interacción en el VPS para confirmar el compromiso de credenciales.



```mermaid

sequenceDiagram

    participant User as Usuario Víctima

    participant Legitimate as Sitio Legítimo (Vulnerable)

    participant Clone as Sitio Clonado (VPS)



    Note over User, Legitimate: 1. Usuario confía en el enlace

    User->>Legitimate: Clic en enlace malicioso (XSS Payload)

    

    Note over Legitimate: 2. Ejecución XSS

    Legitimate->>User: Ejecuta Script de Redirección

    

    Note over User, Clone: 3. Redirección Transparente

    User->>Clone: Carga Sitio Clonado (Typosquatting)

    User->>Clone: Ingresa Credenciales (Simulación)

    

    Note over Clone: 4. Registro de Auditoría

    Clone->>Clone: Log de Evento (Sin guardar pass real)
