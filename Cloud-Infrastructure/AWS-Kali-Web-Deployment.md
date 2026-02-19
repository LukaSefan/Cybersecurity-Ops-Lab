# Despliegue de Infraestructura Cloud (AWS) & Servidor Web Seguro con Arquitectura Zero Trust

## 📋 Resumen del Proyecto
Despliegue integral de un servidor VPS en la nube (AWS EC2) utilizando Kali Linux para operaciones de seguridad ofensiva (Pentesting) y alojamiento web seguro (HTTPS). El proyecto abarca la provisión de infraestructura, configuración de subdominios, certificados SSL automatizados, y un endurecimiento avanzado (Hardening) implementando una arquitectura **Zero Trust** con Tailscale y ModSecurity (WAF).

---

## ⚙️ Especificaciones de Infraestructura

| Componente | Detalle |
| :--- | :--- |
| **Proveedor Cloud** | Amazon Web Services (AWS) - Capa Gratuita |
| **Instancia** | EC2 T3.micro (750 horas/mes gratis) |
| **OS** | Kali Linux (Rolling) - Vía AWS Marketplace |
| **Almacenamiento** | 12 GB EBS (Elastic Block Store) |
| **Servidor Web** | Apache2 + OpenSSL |
| **Seguridad de Red** | AWS Security Groups + UFW + Fail2Ban |
| **Acceso Remoto** | VPN Mesh (Tailscale) - Zero Trust SSH |
| **Seguridad de App** | ModSecurity (WAF) - OWASP CRS |

---

## ☁️ Fase 1: Provisión del Servidor (AWS EC2)

**Reto:** Kali Linux no está disponible en el inicio rápido de AWS.
**Solución:** Suscripción a la AMI oficial a través del AWS Marketplace.

### Configuración del Firewall (Security Groups)
Implementación inicial de reglas de entrada para servicios esenciales (Posteriormente modificadas para Zero Trust).

| Protocolo | Puerto | Uso | Origen |
| :--- | :--- | :--- | :--- |
| **SSH** | 22 | Administración Remota | `Mi IP` (Hardening Inicial) |
| **HTTP** | 80 | Tráfico Web | `0.0.0.0/0` (Internet) |
| **HTTPS** | 443 | Web Segura (SSL) | `0.0.0.0/0` (Internet) |
| **DNS** | 53 | Resolución de Nombres | TCP/UDP |

---

## 🌐 Fase 2: Configuración de Dominio y DNS (Porkbun)

**Objetivo:** Apuntar `sebastianaguilarcv.info` al VPS AWS.
**Problema Detectado:** Conflicto con registros ALIAS/CNAME por defecto de Porkbun (páginas de parking).
**Solución:** Limpieza total de zona DNS y creación de registros A directos.
* **Registro A (@):** Apunta a `3.148.162.101` (Dominio Principal).
* **Registro A (en):** Subdominio para versión internacional.
* **Registro A (login):** Subdominio para portal de acceso.

---

## 🔒 Fase 3: Implementación de SSL/TLS Manual (Apache2)
Despliegue inicial de certificados estáticos para cifrado HTTPS.

### 3.1 Transferencia Segura de Certificados (SCP/SFTP)
Despliegue de llaves criptográficas desde el entorno local (Windows) hacia el servidor Linux.

```bash
# Subida de certificados vía SFTP
sftp> put "C:\Ruta\domain.cert.pem" /home/kali/
sftp> put "C:\Ruta\private.key.pem" /home/kali/
```

### 3.2 Instalación y Hardening en Apache
Mover llaves a directorios protegidos y asignar permisos:

```bash
sudo mv domain.cert.pem /etc/ssl/certs/site.pem
sudo mv private.key.pem /etc/ssl/private/site.key
sudo chmod 600 /etc/ssl/private/site.key
```

Configuración en `/etc/apache2/sites-available/default-ssl.conf`:

```apache
<VirtualHost *:443>
    ServerName sebastianaguilarcv.info
    DocumentRoot /var/www/html
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/site.pem
    SSLCertificateKeyFile /etc/ssl/private/site.key
</VirtualHost>
```

---

## 🌍 Fase 4: Despliegue de Subdominio y Automatización SSL (Certbot)
**Objetivo:** Crear un subdominio `en.sebastianaguilarcv.info` independiente, automatizando el SSL con Let's Encrypt.

### 4.1 Aislamiento de Entorno (VirtualHost)
Para que el subdominio no muestre la web principal, se creó una raíz propia y un archivo de configuración exclusivo.

```bash
# Crear directorio raíz y copiar assets
sudo mkdir -p /var/www/html/en
sudo cp -r /var/www/html/img /var/www/html/en/

# Configuración de VirtualHost exclusivo
sudo nano /etc/apache2/sites-available/en.conf
```

### 4.2 Automatización con Certbot
Migración a gestión automática de certificados.

```bash
# Instalación y ejecución
sudo apt install certbot python3-certbot-apache -y
sudo certbot --apache
```
* **Troubleshooting Rutas:** Certbot copió el DocumentRoot por defecto. Se corrigió editando `/etc/apache2/sites-available/en-le-ssl.conf` para que apunte a `/var/www/html/en`.
* **Troubleshooting Descargas:** Se corrigió el botón de descarga del CV usando rutas absolutas en el HTML (`href="/Documentos/CV_PROFESIONAL.pdf"`) para evitar errores 404 en el subdominio.

---

## 🛡️ Fase 5: Blindaje de Gestión (Arquitectura Zero Trust)
**Objetivo:** Eliminar la exposición del puerto 22 (SSH) a Internet y eliminar la dependencia de llaves `.pem`.

### 5.1 Configuración de Tailscale (VPN Mesh)

```bash
curl -fsSL [https://tailscale.com/install.sh](https://tailscale.com/install.sh) | sh
sudo tailscale up --ssh --reset
```
* **Ventaja:** Tailscale gestiona la identidad SSH basándose en el usuario logueado en la red mesh. La conexión es directa y cifrada (`ssh kali@100.x.x.x`).

### 5.2 Hardening Extremo en AWS Security Group
Se editó la regla SSH en el firewall de AWS para aislar el puerto:
* **Puerto:** 22 (TCP)
* **Origen:** `100.64.0.0/10` (Rango exclusivo de Tailscale).
* **Resultado:** El puerto 22 es ahora invisible para escáneres públicos (Nmap/Shodan).

---

## 🧱 Fase 6: Hardening del Host y Seguridad de Aplicación (WAF)

### 6.1 Mitigación Activa con Fail2Ban
**Objetivo:** Bloquear ataques de fuerza bruta y escaneos agresivos.

```bash
sudo apt install fail2ban -y
```

Se configuró una lista blanca en `/etc/fail2ban/jail.local` para evitar auto-bloqueos:

```ini
ignoreip = 127.0.0.1/8 ::1 192.168.18.0/24 100.0.0.0/8
bantime = 1h
maxretry = 5
```

### 6.2 ModSecurity (Web Application Firewall)
Protección contra ataques de capa 7 (Inyección SQL, XSS, RCE) usando el OWASP Core Rule Set.

```bash
sudo apt install libapache2-mod-security2 modsecurity-crs -y
sudo cp /etc/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf
```

* Se cambió `SecRuleEngine DetectionOnly` a `SecRuleEngine On` para activar el modo bloqueo.
* **Prueba de Inyección:** Acceder a `http://midominio.com/?exec=/bin/bash` generó exitosamente un Error 403 Forbidden, confirmando la interceptación del WAF.

---

## 📊 Resumen de Estado de Infraestructura

| Componente | Estado | Seguridad |
| :--- | :--- | :--- |
| **SSH** | Activo (Tailscale) | Zero Trust (Invisible al mundo) |
| **HTTP/S** | Activo (Apache) | WAF (ModSecurity) / SSL Automático |
| **Acceso Externo** | Cerrado | Solo vía VPN Mesh |
