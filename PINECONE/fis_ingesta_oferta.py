"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v7.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Ingesta Vectorial de Alta Fidelidad (Fix Model Name)
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
=============================================================================
"""

import os
import sys
import time
import json
import pandas as pd
from dotenv import load_dotenv
from google import genai
from pinecone import Pinecone

# --- FIX DE RUTAS ---
directorio_actual = os.path.dirname(os.path.abspath(__file__))
directorio_raiz = os.path.dirname(directorio_actual)
if directorio_raiz not in sys.path:
    sys.path.append(directorio_raiz)

load_dotenv(os.path.join(directorio_raiz, '.env'))

# --- CONFIGURACIÓN CRÍTICA ---
# Cambiamos al modelo que tu diagnóstico marcó como EXISTENTE (no 404)
MODELO_ALTA_FIDELIDAD = "gemini-embedding-2-preview" 
NAMESPACE_UR = "catalogo-oferta-ur"
ARCHIVO_PROGRESO = os.path.join(directorio_actual, "progreso_ingesta_3072.json")

def ejecutar_ingesta_resiliente():
    print(f"\n{'='*75}\n🚀 INGESTA SYMBIOMEMESIS V7 - MODELO: {MODELO_ALTA_FIDELIDAD}\n{'='*75}")
    
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    client_gemini = genai.Client(api_key=api_key)
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY").strip())
    indice = pc.Index(os.getenv("PINECONE_INDEX").strip())
    
    ruta_excel = os.path.join(directorio_raiz, "data", "OFERTA ACADEMICA ASIGNATURAS 2024.xlsx")
    df_raw = pd.read_excel(ruta_excel, sheet_name="ClasificaAsignaturas2024UR")
    df_agrupado = df_raw.groupby(['FACULTAD_ASIGNATURA', 'NOMBRE_PROGRAMA', 'NOMBRE_ASIGNATURA']).size().reset_index(name='Grupos')
    
    total = len(df_agrupado)
    lote = []
    
    # Checkpoint
    inicio = 0
    if os.path.exists(ARCHIVO_PROGRESO):
        with open(ARCHIVO_PROGRESO, 'r') as f: inicio = json.load(f).get("ultimo_indice", 0)

    print(f"[*] Registros: {total}. Retomando desde: {inicio}")

    for idx, row in df_agrupado.iterrows():
        if idx < inicio: continue

        time.sleep(0.7) # Pacing para evitar bloqueos por ráfaga

        texto = f"Facultad: {row['FACULTAD_ASIGNATURA']}. Programa: {row['NOMBRE_PROGRAMA']}. Asignatura: {row['NOMBRE_ASIGNATURA']}."
        
        try:
            # Generación de Embedding
            res = client_gemini.models.embed_content(model=MODELO_ALTA_FIDELIDAD, contents=texto)
            vector = res.embeddings[0].values

            lote.append({
                "id": f"ur_v7_{idx}", 
                "values": vector, 
                "metadata": {"facultad": str(row['FACULTAD_ASIGNATURA']), "programa": str(row['NOMBRE_PROGRAMA']), "asignatura": str(row['NOMBRE_ASIGNATURA'])}
            })

            if len(lote) >= 40 or idx == total - 1:
                indice.upsert(vectors=lote, namespace=NAMESPACE_UR)
                with open(ARCHIVO_PROGRESO, 'w') as f: json.dump({"ultimo_indice": idx + 1}, f)
                print(f"[\033[92m{((idx+1)/total)*100:.1f}%\033[0m] Sincronizado lote hasta registro {idx+1}")
                lote = []

        except Exception as e:
            if "429" in str(e) or "spending cap" in str(e).lower():
                print(f"\n⚠️ BLOQUEO DE CUOTA/GASTO: Google Cloud detuvo la petición. Pausa de 60s...")
                time.sleep(60)
                continue
            else:
                print(f"❌ Error crítico en registro {idx}: {e}")
                break

if __name__ == "__main__":
    ejecutar_ingesta_resiliente()