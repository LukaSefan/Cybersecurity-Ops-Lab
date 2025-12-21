# Despliegue de Servidor NAS Seguro & Hardening de Linux

## 📋 Resumen del Proyecto
Transformación de hardware reutilizado en un servidor de almacenamiento centralizado (NAS) de alta disponibilidad. El proyecto integra orquestación de servicios (CasaOS), almacenamiento unificado (MergerFS), sincronización de nube privada y seguridad perimetral mediante VPN Mesh.

## ⚙️ Especificaciones Técnicas
| Componente | Detalle |
| :--- | :--- |
| **CPU** | Intel Pentium G2020 (Dual Core) |
| **RAM** | 4GB DDR3 |
| **OS** | Ubuntu Server 24.04 (Headless) + CasaOS GUI |
| **Almacenamiento** | 1.4 TB Pool (MergerFS) + 230GB System Disk |
| **Rol** | NAS, Private Cloud, Docker Host |

---
Recuperación de hardware: Se restauró una PC antigua, realizando limpieza profunda, cambio de pasta térmica y ensamblaje de 3 discos duros para el pool de almacenamiento.

## 🏗️ Fase 1: Orquestación (CasaOS)
Instalación del dashboard para gestión de contenedores.

curl -fsSL https://get.casaos.io | sudo bash


## ☁️ Fase 2: Nube Privada (Syncthing)
Sincronización de archivos (iOS/PC) sin intermediarios.
* **Configuración:** Mapeo de volúmenes Docker hacia `/mnt/Total_Espacio` para almacenamiento persistente y corrección de permisos para acceso LAN.

## 🔐 Fase 3: Acceso Remoto (Tailscale VPN)
Acceso seguro y bypass de CGNAT sin abrir puertos.

Instalación
curl -fsSL https://tailscale.com/install.sh | sh

Habilitar IP Forwarding
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf sudo sysctl -p /etc/sysctl.d/99-tailscale.conf

Publicar rutas y activar Exit Node
sudo tailscale up --advertise-exit-node --advertise-routes=192.168.18.0/24 --reset


## 💾 Fase 4: Almacenamiento Unificado (MergerFS)
Creación de un pool de 1.4TB sumando discos heterogéneos (400GB + 1TB).

Instalación
sudo apt update && sudo apt install mergerfs fuse -y sudo mkdir /mnt/Total_Espacio


**Configuración persistente (`/etc/fstab`):**
1. Discos Físicos
/dev/sdb1 /mnt/disco_omv auto defaults,nofail 0 0 /dev/sdc /mnt/disco_1tb ext4 defaults,nofail 0 0

2. Pool MergerFS
/mnt/disco_omv:/mnt/disco_1tb /mnt/Total_Espacio fuse.mergerfs defaults,allow_other,nofail,use_ino,category.create=mfs,moveonenospc=true,minfreespace=10G 0 0


## 🛡️ Fase 5: Seguridad (Fail2Ban & Energía)
Bloqueo de intrusos y gestión de energía.

Instalación Fail2Ban
sudo apt install fail2ban -y

Evitar suspensión automática (Server 24/7)
sudo systemctl mask sleep.target suspend.target hibernate.target


**Reglas de bloqueo SSH (`jail.local`):**
[sshd] enabled = true bantime = 1h maxretry = 5 ignoreip = 127.0.0.1/8 192.168.18.0/24 100.0.0.0/8
