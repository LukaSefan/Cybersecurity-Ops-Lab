# Despliegue de Infraestructura Cloud (AWS) & Servidor Web Seguro

## 📋 Resumen del Proyecto
Despliegue de un servidor VPS en la nube (AWS EC2) utilizando Kali Linux para operaciones de seguridad ofensiva (Pentesting) y alojamiento web seguro (HTTPS). El proyecto abarca desde la provisión de infraestructura hasta la configuración de certificados SSL y DNS.

## ⚙️ Especificaciones de Infraestructura
| Componente | Detalle |
| :--- | :--- |
| **Proveedor Cloud** | Amazon Web Services (AWS) - Capa Gratuita |
| **Instancia** | EC2 T3.micro (750 horas/mes gratis) |
| **OS** | Kali Linux (Rolling) - Vía AWS Marketplace |
| **Almacenamiento** | 12 GB EBS (Elastic Block Store) |
| **Servidor Web** | Apache2 + OpenSSL |

---

## ☁️ Fase 1: Provisión del Servidor (AWS EC2)
**Reto:** Kali Linux no está disponible en el inicio rápido de AWS.
**Solución:** Suscripción a la AMI oficial a través del AWS Marketplace.

### Configuración del Firewall (Security Groups)
Implementación de reglas de entrada estrictas para servicios esenciales.

| Protocolo | Puerto | Uso | Origen |
| :--- | :--- | :--- | :--- |
| **SSH** | 22 | Administración Remota | Mi IP (Hardening) |
| **HTTP** | 80 | Tráfico Web | 0.0.0.0/0 (Internet) |
| **HTTPS** | 443 | Web Segura (SSL) | 0.0.0.0/0 (Internet) |
| **DNS** | 53 | Resolución de Nombres | TCP/UDP |

## 🔑 Fase 2: Gestión de Accesos (SSH Hardening)
Transición de autenticación basada solo en llaves (.pem) a autenticación híbrida para facilitar el acceso administrativo seguro.

1. Conexión inicial con llave PEM
ssh -i "llave-kali-AWS.pem" kali@3.148.162.101

2. Habilitar autenticación por contraseña en /etc/ssh/sshd_config
Cambiar: PasswordAuthentication no -> yes
3. Reiniciar servicio
sudo systemctl restart sshd


## 🌐 Fase 3: Configuración de Dominio y DNS (Porkbun)
**Objetivo:** Apuntar `sebastianaguilarcv.info` al VPS AWS.
**Problema Detectado:** Conflicto con registros ALIAS/CNAME por defecto de Porkbun.
**Solución:** Limpieza de zona DNS y creación de registros A directos.

* **Registro A (@):** Apunta a `3.148.162.101`
* **Registro A (login):** Subdominio para portal de acceso.

## 🔒 Fase 4: Implementación de SSL/TLS (Apache2)
Despliegue de certificados Let's Encrypt para cifrado HTTPS.

### 4.1 Transferencia Segura de Certificados (SCP/SFTP)
Despliegue de llaves criptográficas desde entorno local (Windows) hacia el servidor Linux.

Subida de certificados vía SFTP
put "C:\Ruta\domain.cert.pem" /home/kali/ put "C:\Ruta\private.key.pem" /home/kali/


### 4.2 Instalación y Hardening en Apache
Configuración de VirtualHosts para forzar redirección HTTPS y uso de llaves.

Mover llaves a directorios protegidos
sudo mv domain.cert.pem /etc/ssl/certs/site.pem sudo mv private.key.pem /etc/ssl/private/site.key sudo chmod 600 /etc/ssl/private/site.key

Configuración en /etc/apache2/sites-available/default-ssl.conf
<VirtualHost *:443> ServerName sebastianaguilarcv.info SSLEngine on SSLCertificateFile /etc/ssl/certs/site.pem SSLCertificateKeyFile /etc/ssl/private/site.key </VirtualHost>


### 4.3 Despliegue Final
sudo a2enmod ssl sudo a2ensite default-ssl.conf sudo systemctl restart apache2

*Resultado:* Sitio web accesible con cifrado robusto (Candado Verde).
