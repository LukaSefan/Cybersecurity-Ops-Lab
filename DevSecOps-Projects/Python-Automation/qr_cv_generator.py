import qrcode
import os
import sys

# CONFIGURACIÓN 
URL_A_CODIFICAR = 'sebastianaguilarcv.info'
NOMBRE_ARCHIVO = 'cv_sebastian.png'
CARPETA_DESTINO = 'QRs_Generados'


def generar_qr():
    try:
        # 1. Crear la carpeta si no existe
        if not os.path.exists(CARPETA_DESTINO):
            os.makedirs(CARPETA_DESTINO)
            print(f"[+] Carpeta '{CARPETA_DESTINO}' creada.")

        # 2. Generar el QR
        print(f"[*] Generando QR para: {URL_A_CODIFICAR}...")
        img = qrcode.make(URL_A_CODIFICAR)

        # 3. Guardar el archivo
        ruta_final = os.path.join(CARPETA_DESTINO, NOMBRE_ARCHIVO)
        img.save(ruta_final)

        print(f"\n[+] ÉXITO: Código QR guardado en: {ruta_final}")
        
    except Exception as e:
        print(f"[-] ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    generar_qr()
