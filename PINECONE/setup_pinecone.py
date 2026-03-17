"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v7.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Configuración de Infraestructura Vectorial (Pinecone Setup)
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Prepara el índice de Pinecone para la v7.0.
    Ajustado para Gemini 2.0 (3072 dimensiones) para RAG de alta fidelidad.
=============================================================================
"""

import os
import time
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# --- INTEGRACIÓN CON TELEMETRÍA (Opcional para Setup) ---
try:
    from fis_telemetria_v7 import TelemetriaMaestraV7 as TM, ColoresUR
except ImportError:
    class TM:
        @staticmethod
        def encabezado(t): print(f"\n=== {t} ===")
        @staticmethod
        def evento(a, m, color=""): print(f"[{a}] {m}")
        @staticmethod
        def error(m): print(f"❌ ERROR: {m}")

# Cargar configuración
ruta_env = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(ruta_env)

def configurar_pinecone_v7():
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX", "symbiomemesis-v7-index")
    
    if not api_key:
        TM.error("No se encontró PINECONE_API_KEY en el archivo .env")
        return

    pc = Pinecone(api_key=api_key)
    
    TM.encabezado("CONFIGURACIÓN DE INFRAESTRUCTURA VECTORIAL V7")
    TM.evento("SISTEMA", f"Conectando a Pinecone Cloud...")

    # --- VERIFICACIÓN Y CREACIÓN ---
    try:
        indices_existentes = pc.list_indexes().names()
        
        if index_name not in indices_existentes:
            TM.evento("SISTEMA", f"Creando índice '{index_name}' para Gemini 2.0...")
            
            # DIMENSIÓN 3072: Requisito crítico para gemini-embedding-2-preview
            pc.create_index(
                name=index_name,
                dimension=3072, 
                metric="cosine", 
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1" 
                )
            )
            
            # Espera activa (Polling)
            with TM.monitor(None, "INFRAESTRUCTURA", "Creacion_Indice") as m:
                while not pc.describe_index(index_name).status['ready']:
                    TM.evento("PINECONE", "Esperando a que el índice esté listo (Status: INITIALIZING)...")
                    time.sleep(5)
            
            TM.evento("SISTEMA", f"✅ Índice '{index_name}' creado con 3072 dimensiones.")
        else:
            descripcion = pc.describe_index(index_name)
            dim_actual = descripcion.dimension
            
            if dim_actual != 3072:
                TM.error(f"¡ALERTA DE CAJA BLANCA! El índice existe pero tiene {dim_actual} dimensiones.")
                TM.evento("CONSEJO", "Para Symbiomemesis v7.0 (3072 dim), debe borrar el índice antiguo o cambiar el nombre en el .env.")
            else:
                TM.evento("SISTEMA", f"✅ El índice '{index_name}' ya está configurado correctamente (3072 dim).")

    except Exception as e:
        TM.error(f"Fallo crítico en la configuración de Pinecone: {str(e)}")

if __name__ == "__main__":
    configurar_pinecone_v7()