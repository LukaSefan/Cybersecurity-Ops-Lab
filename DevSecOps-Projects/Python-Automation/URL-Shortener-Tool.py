import requests
import sys

# ==========================================
# HERRAMIENTA DE AUTOMATIZACIÓN: URL SHORTENER
# Autor: Sebastián Aguilar
# Descripción: Script para acortar URLs usando múltiples APIs (TinyURL & Is.gd)
# ==========================================

def acortar_tinyurl(url_larga):
    """Acorta usando el API de TinyURL"""
    api_url = 'http://tinyurl.com/api-create.php?url='
    try:
        response = requests.get(api_url + url_larga, timeout=10)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return f"[!] Error TinyURL: {response.status_code}"
    except Exception as e:
        return f"[!] Error de conexión: {str(e)}"

def acortar_isgd(url_larga):
    """Acorta usando el API de Is.gd (Corregido parameter handling)"""
    api_url = 'https://is.gd/api.php'
    payload = {'longurl': url_larga, 'format': 'simple'}
    try:
        response = requests.get(api_url, params=payload, timeout=10)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return f"[!] Error Is.gd: {response.text.strip()}"
    except Exception as e:
        return f"[!] Error de conexión: {str(e)}"

def main():
    print("--- AUTOMATIZACIÓN DE ACORTADORES ---")
    url = input("Ingrese la URL larga a acortar: ")
    
    print("\n[1] Procesando con TinyURL...")
    res_tiny = acortar_tinyurl(url)
    print(f"✅ Resultado: {res_tiny}")

    print("\n[2] Procesando con Is.gd...")
    res_isgd = acortar_isgd(url)
    print(f"✅ Resultado: {res_isgd}")

if __name__ == "__main__":
    main()
