# 🌐 Fundamentos de Arquitectura de Red y Segmentación

### 📋 Introducción
Documentación técnica sobre los principios de diseño de redes aplicados en el laboratorio. Se detalla la segmentación de tráfico (*Broadcast Domains* vs. *Collision Domains*), el rol del enrutamiento y la estructura física de una red empresarial segura.

---

### 🛡️ 1. Segmentación de Red (Subnetting)

El principio de **"Defensa en Profundidad"** comienza en la red. Una red plana (*Flat Network*) es un riesgo de seguridad crítico.

#### Concepto: Broadcast Domain vs. Subnets

| Estado | Descripción |
| :--- | :--- |
| **🚨 Problema** | **(Broadcast Domain):** En una red plana, cualquier paquete de difusión (ARP requests, DHCP discovery) llega a todos los hosts. Esto genera ruido ("ruido en la fiesta") y permite que un atacante en un nodo escuche tráfico de toda la red. |
| **✅ Solución** | **(Subnetting):** División lógica de la red para aislar el tráfico y mejorar el rendimiento y seguridad. |

> **Router (Gateway):** Actúa como frontera de seguridad (*El Portero*). Filtra el tráfico entre segmentos mediante ACLs (Listas de Control de Acceso) o reglas de Firewall, impidiendo que el tráfico de broadcast sature la red.

---

### 🏗️ 2. Topología Física y Lógica

#### Flujo de Tráfico Empresarial
La arquitectura implementada sigue el estándar jerárquico:
`ISP (Internet) ➡️ Router (Capa 3) ➡️ Switch (Capa 2) ➡️ Endpoints / APs`

#### Especificaciones de Capas

| Capa | Tecnología | Función Principal |
| :--- | :--- | :--- |
| **Capa Física (L1)** | Cableado Cat 6 | Garantizar ancho de banda de **1Gbps/10Gbps** y reducir la diafonía (interferencia). |
| **Capa de Enlace (L2)** | Switching | El Switch distribuye tráfico basándose en **direcciones MAC** dentro de su propio segmento. |
| **Capa de Red (L3)** | Routing | El Router toma decisiones de reenvío entre diferentes subredes (ej: `192.168.10.0/24` Ventas vs `192.168.20.0/24` TI). |

---

### 🎛️ 3. Infraestructura Centralizada (Rack)

La centralización del cableado mediante **Patch Panels** permite flexibilidad y seguridad física.

* **Gestión:** Permite mover un host (ej: Oficina 305) de una VLAN a otra simplemente cambiando el parcheo en el rack, sin reconfigurar el dispositivo final.
* **Seguridad:** Punto único de monitoreo para **IDS/IPS** (Sistemas de Detección de Intrusos).

---

### 📡 4. Wireless & Access Points (APs)

* **Rol del AP:** Funciona como un puente (*Bridge*) transparente entre el medio inalámbrico (802.11) y el cableado (802.3).
* **Puertos LAN en AP:** Actúan como un switch no gestionado para conveniencia local, extendiendo el mismo dominio de broadcast del SSID.

> 🔒 **Nota de Seguridad:**
> En este laboratorio, se aplica el principio de **Mínimo Privilegio** a nivel de red, asegurando que los dispositivos IoT estén aislados de la red de servidores críticos.
