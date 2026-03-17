import os
from dotenv import load_dotenv
from google import genai

def ejecutar_diagnostico():
    print("\n=======================================================")
    print(" 🩺 DIAGNÓSTICO DE CONEXIÓN GEMINI (EMBEDDINGS) ")
    print("=======================================================")
    
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    
    if not api_key:
        print("❌ ERROR CRÍTICO: No se encontró la GOOGLE_API_KEY en tu archivo .env.")
        return

    print(f"[*] Llave detectada. Iniciando cliente genai...\n")
    client = genai.Client(api_key=api_key)

    # Vamos a probar todos los nombres de modelo que Google ha usado recientemente
    modelos_candidatos = [
        "text-embedding-004",
        "models/text-embedding-004",
        "gemini-embedding-2",
        "models/gemini-embedding-2",
        "gemini-embedding-2-preview",
        "text-embedding-004-preview"
    ]

    for modelo in modelos_candidatos:
        print(f"Probando modelo: {modelo:<28} -> ", end="")
        try:
            # Intentamos vectorizar un texto simple
            res = client.models.embed_content(
                model=modelo, 
                contents="Prueba de conexión UR"
            )
            dimensiones = len(res.embeddings[0].values)
            print(f"✅ ¡ÉXITO! (Vector de {dimensiones} dimensiones)")
            print(f"\n🚀 EL NOMBRE CORRECTO QUE DEBEMOS USAR ES: '{modelo}'")
            return # Si funciona, terminamos el diagnóstico
            
        except Exception as e:
            # Extraemos el código de error para que no ensucie mucho la pantalla
            error_msg = str(e)
            if "404" in error_msg:
                print("❌ 404 NOT FOUND")
            elif "429" in error_msg:
                print("❌ 429 CUOTA EXCEDIDA (Aún te leen como Free Tier)")
            elif "400" in error_msg:
                print("❌ 400 BAD REQUEST (Nombre de método no soportado)")
            else:
                print(f"❌ ERROR: {error_msg}")

if __name__ == "__main__":
    ejecutar_diagnostico()