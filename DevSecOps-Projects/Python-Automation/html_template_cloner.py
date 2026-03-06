#!/usr/bin/env python3
"""
# -----------------------------------------------------------------------------
# TOOL: HTML Template Cloner & Consolidator
# AUTHOR: Sebastian Aguilar
# DESCRIPTION: Clones a target website and consolidates external CSS and JS 
#              into a single, standalone HTML file. Ideal for generating 
#              offline templates or Red Team landing pages (e.g., Gophish).
# STATUS: Educational & Authorized Audits Only
# -----------------------------------------------------------------------------
"""

import requests
from bs4 import BeautifulSoup, Comment
import os
from urllib.parse import urljoin
import urllib3

# Desactivar advertencias de certificados (Útil para laboratorios con SSL auto-firmado)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def clonar_organizado(dominio):
    ruta_carpeta = "dominios-html"
    os.makedirs(ruta_carpeta, exist_ok=True)
    archivo_salida = os.path.join(ruta_carpeta, f"{dominio}.html")
    
    session = requests.Session()
    session.verify = False 
    
    # Evasión básica: Simular ser un navegador real
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    })

    print(f"[*] 🌐 Conectando a: {dominio}...")

    try:
        url_objetivo = f"https://www.{dominio}" if not dominio.startswith('www.') else f"https://{dominio}"
        resp = session.get(url_objetivo, timeout=15)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.text, 'html.parser')

        # 1. Limpieza de comentarios (Reducción de huella)
        for comentario in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comentario.extract()

        # 2. Unificar CSS en el <head> (Inlining)
        print("[*] 🎨 Procesando estilos CSS...")
        estilos_unificados = ""
        
        for css in soup.find_all('link'):
            try:
                if css.has_attr('rel') and 'stylesheet' in css.get('rel'):
                    href = css.get('href')
                    if href:
                        css_url = urljoin(url_objetivo, href)
                        css_resp = session.get(css_url, timeout=5)
                        if css_resp.status_code == 200:
                            estilos_unificados += f"\n/* Fuente: {css_url} */\n{css_resp.text}"
                            css.decompose() # Remueve el link externo original
            except Exception:
                continue
        
        estilo_tag = soup.new_tag('style')
        estilo_tag.string = estilos_unificados
        if soup.head:
            soup.head.append(estilo_tag)
        elif soup.html:
            head = soup.new_tag('head')
            soup.html.insert(0, head)
            head.append(estilo_tag)

        # 3. Unificar Scripts al final del <body> (Inlining JS)
        print("[*] ⚡ Procesando scripts JS...")
        scripts_externos = ""
        for script in soup.find_all('script'):
            try:
                src = script.get('src')
                if src:
                    js_url = urljoin(url_objetivo, src)
                    js_resp = session.get(js_url, timeout=5)
                    if js_resp.status_code == 200:
                        scripts_externos += f"\n// Fuente: {js_url}\n{js_resp.text}"
                        script.decompose() # Remueve el script externo original
            except Exception:
                continue
        
        nuevo_script_tag = soup.new_tag('script')
        nuevo_script_tag.string = scripts_externos
        if soup.body:
            soup.body.append(nuevo_script_tag)

        # 4. Guardar archivo con formato legible
        print("[*] 💾 Generando archivo HTML final...")
        html_final = soup.prettify()
        
        with open(archivo_salida, "w", encoding="utf-8", errors="ignore") as f:
            f.write(html_final)

        print(f"\n[+] ✅ ¡ÉXITO! Archivo consolidado en: {archivo_salida}")

    except Exception as e:
        print(f"[-] ❌ Error crítico: {e}")

if __name__ == "__main__":
    print("--- HTML TEMPLATE CLONER ---")
    # OPSEC: Evitar sugerir dominios reales en el prompt
    entrada = input("Pega el dominio (ej: target-domain.com): ").strip()
    dominio = entrada.replace('https://', '').replace('http://', '').split('/')[0]
    
    if dominio:
        clonar_organizado(dominio)
