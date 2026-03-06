# 🛡️ Cybersecurity Operations Lab
> **Technical Portfolio:** Cloud Infrastructure, Malware Research, Ethical Hacking & Automation.

Welcome to my personal Security Operations (SecOps) lab. This repository centralizes technical documentation, Proof of Concepts (PoC), and infrastructure deployments aimed at refining **Red Teaming** and **Secure Architecture** skills.

---

## 📂 Project Modules

### 1. ⚔️ Offensive Security (Red Team & Pentesting)
*Location: `/Hacking-Module`*
Documentation of TTPs (Tactics, Techniques, and Procedures) for security audits.
* **Defense Evasion:** **HTML Smuggling** technique to bypass email filters and sandboxes.
* **Malware Development:** Research on **C++ loaders with RC4 encryption** to evade static signatures.
* **Wireless Audit:** Methodology for WPA2 handshake capture and **Evil Twin** deployment with captive portal.
* **Web Hacking:** Kill Chain using **Reflected XSS + Open Redirect** in real-world environments.

### 2. ☁️ Cloud Infrastructure & Hardening
*Location: `/Cloud-Infrastructure`, `/Infrastructure-HomeLab` & `/Infrastructure-Defense`*
Deployment and securing of cloud and on-premise servers.
* **AWS Cloud:** Deployment of EC2 instances for pentesting (Kali Linux) with Security Groups and SSH key management.
* **HomeLab Server:** Construction of a secure NAS server using **Ubuntu Server**, storage management (MergerFS), and remote access via **Mesh VPN (Tailscale)**.
* **Blue Team & WAF Evasion:** Research on [Nginx Hardening and Filter Evasion](./Infrastructure-Defense) for critical infrastructure protection.

### 3. 🤖 AI Security Research
*Location: `/AI-Security-Lab`*
Exploration of Generative AI applied to cybersecurity.
* **Local LLMs:** Implementation of "Uncensored" models (Dolphin/Llama3) locally (Air-gapped) for adversary simulation and offensive script generation without telemetry.

### 4. 🐍 DevSecOps & Automation
*Location: `/DevSecOps-Projects/Python-Automation`*
Development of custom tools and secure software architectures.
* **Scripting:** Automation tools in **Python** (URL Shorteners, QR Code / CV Generators, **Web Cloning & HTML Smuggling Payload Generators**).
* **Secure Architecture:** Design documentation for E-Commerce applications (MVC, .NET, Backend Security).

---
*(Spanish version below)*
<br>
<br>


# 🛡️ Cybersecurity Operations Lab

> **Portafolio Técnico:** Infraestructura Cloud, Investigación de Malware, Hacking Ético y Automatización.

Bienvenido a mi laboratorio personal de operaciones de seguridad (SecOps). Este repositorio centraliza documentación técnica, pruebas de concepto (PoC) y despliegues de infraestructura que realizo para perfeccionar mis habilidades en **Red Teaming** y **Arquitectura Segura**.

---

## 📂 Módulos del Proyecto

### 1. ⚔️ Seguridad Ofensiva (Red Team & Pentesting)
*Ubicación: `/Hacking-Module`*
Investigación y documentación de Tácticas, Técnicas y Procedimientos (TTPs) para auditorías de seguridad.
* **Evasión de Defensas:** Técnica de **HTML Smuggling** para bypass de filtros de correo y sandboxes.
* **Malware Development:** Investigación sobre loaders en **C++ con cifrado RC4** para evasión de firmas estáticas.
* **Auditoría Wireless:** Metodología para captura de handshakes WPA2 y despliegue de **Evil Twin** con portal cautivo.
* **Web Hacking:** Cadena de ataque (Kill Chain) utilizando **XSS Reflejado + Open Redirect** en entornos reales.

### 2. ☁️ Infraestructura Cloud & Hardening
*Ubicación: `/Cloud-Infrastructure`, `/Infrastructure-HomeLab` & `/Infrastructure-Defense`*
Despliegue y aseguramiento de servidores en la nube y entornos locales (On-Premise).
* **AWS Cloud:** Despliegue de instancias EC2 para pentesting (Kali Linux) con gestión de Security Groups y llaves SSH.
* **HomeLab Server:** Construcción de un servidor NAS seguro con **Ubuntu Server**, gestión de almacenamiento (MergerFS) y acceso remoto vía **VPN Mesh (Tailscale)**.
* **Blue Team & WAF Evasion:** Investigación sobre [Hardening de Nginx y Evasión de Filtros](./Infrastructure-Defense) para protección de infraestructura crítica.

### 3. 🤖 AI Security Research
*Ubicación: `/AI-Security-Lab`*
Exploración de Inteligencia Artificial Generativa aplicada a la ciberseguridad.
* **Local LLMs:** Implementación de modelos "Uncensored" (Dolphin/Llama3) en local (Air-gapped) para simulación de adversarios y generación de scripts ofensivos sin telemetría.

### 4. 🐍 DevSecOps & Automatización
*Ubicación: `/DevSecOps-Projects/Python-Automation`*
Desarrollo de herramientas propias y arquitecturas de software seguro.
* **Scripting:** Herramientas de automatización en **Python** (Acortadores de URL, Generador de Códigos QR, **Clonación Web y Generación de Payloads HTML Smuggling**).
* **Arquitectura Segura:** Documentación de diseño para aplicaciones E-Commerce (MVC, .NET, Seguridad en Backend).

---

## 🛠️ Stack Tecnológico
* **Lenguajes:** Python, C++, Bash, HTML/JS.
* **Sistemas:** Kali Linux, Ubuntu Server, Windows Server.
* **Cloud & Virtualización:** AWS (EC2), Docker, CasaOS.
* **Herramientas:** Metasploit, Bettercap, Aircrack-ng, Wireshark, Burp Suite.

---

> **⚠️ Disclaimer Legal / Descargo de Responsabilidad**
>
> Todo el material, código y documentación alojada en este repositorio tiene fines estrictamente **educativos y de investigación**. Las técnicas ofensivas descritas han sido ejecutadas exclusivamente en **entornos de laboratorio controlados** y con dispositivos propios.
>
> El autor no se hace responsable del mal uso de la información aquí expuesta. El acceso no autorizado a sistemas informáticos es un delito.
