"""
=============================================================================
DIAGNÓSTICO FORENSE: CATÁLOGO DE MODELOS GEMINI
=============================================================================
"""
import os
import requests
from dotenv import load_dotenv

def auditar_modelos_gemini():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("❌ ERROR: No se encontró GOOGLE_API_KEY en el .env")
        return

    # Ocultamos parte de la llave por seguridad
    llave_enmascarada = f"{api_key[:10]}...{api_key[-5:]}"
    print(f"🔑 Probando autenticación con llave: {llave_enmascarada}\n")

    # Endpoint oficial de Google Generative Language API
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    print("📡 Conectando con los servidores de Google AI Studio...")
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        datos = respuesta.json()
        print("\n✅ LLAVE VÁLIDA. Modelos de generación de texto soportados:\n")
        print("Copie EXACTAMENTE el nombre de la derecha en su archivo .env:")
        print("-" * 60)
        
        for modelo in datos.get('models', []):
            metodos = modelo.get('supportedGenerationMethods', [])
            # Solo nos interesan los modelos que generan texto/contenido
            if 'generateContent' in metodos:
                nombre_crudo = modelo['name']
                # Limpiamos el prefijo 'models/' para el .env
                nombre_limpio = nombre_crudo.replace('models/', '')
                print(f"  👉 {nombre_limpio}")
                
        print("-" * 60)
    else:
        print(f"\n❌ ERROR DE AUTENTICACIÓN: {respuesta.status_code}")
        print(respuesta.json())

if __name__ == "__main__":
    auditar_modelos_gemini()