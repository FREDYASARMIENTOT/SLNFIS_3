"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v7.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Agente de Inicialización de Memoria Vectorial (Alta Fidelidad 3072)
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Puntal de infraestructura que recrea el índice en Pinecone con 3072 
    dimensiones para soportar el modelo text-embedding-004 de Google.
=============================================================================
"""

import os
import sys
import time
from datetime import datetime

# --- 🛠️ CORRECCIÓN DE RUTAS (PATH FIX) ---
# Permite que el script encuentre fis_cintagentica_v7 en la raíz del proyecto
directorio_actual = os.path.dirname(os.path.abspath(__file__))
directorio_raiz = os.path.dirname(directorio_actual)
if directorio_raiz not in sys.path:
    sys.path.append(directorio_raiz)

from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from fis_cintagentica_v7 import MallaCognitivaCompartida

try:
    from infra.console import InterfazTerminal as ConsolaDelSistema
except ImportError:
    class ConsolaDelSistema:
        @staticmethod
        def mostrar_log(msg): print(f"[\033[94mLOG\033[0m] {msg}")

# Cargar configuración desde la raíz (.env)
load_dotenv(os.path.join(directorio_raiz, '.env'))

class AgenteInicializadorMemoriaV7:
    """
    Arquitecto de la Memoria a Largo Plazo del enjambre.
    Configura el espacio vectorial para máxima resolución semántica.
    """

    def __init__(self):
        self.api_key = os.getenv("PINECONE_API_KEY", "").strip()
        self.index_name = os.getenv("PINECONE_INDEX", "symbiomemesis-v7-index").strip()
        
        # 🚀 CONFIGURACIÓN DE ALTA RESOLUCIÓN PARA TESIS
        self.dimension = 3072  # Estándar para text-embedding-004
        self.metric = "cosine" # Optimizado para similitud semántica

        if not self.api_key:
            raise ValueError("❌ Error: PINECONE_API_KEY no encontrada en el .env")

        self.pc = Pinecone(api_key=self.api_key)

    def purgar_y_recrear_indice(self):
        """Elimina el índice de 768 y crea el de 3072."""
        ConsolaDelSistema.mostrar_log(f"Consultando estado de infraestructura en Pinecone...")
        
        # 1. Limpieza de índices previos
        indices_actuales = [idx.name for idx in self.pc.list_indexes()]
        if self.index_name in indices_actuales:
            ConsolaDelSistema.mostrar_log(f"⚠️ Detectado índice con dimensiones incompatibles. ELIMINANDO...")
            self.pc.delete_index(self.index_name)
            ConsolaDelSistema.mostrar_log("Esperando 15s para propagación de borrado en la nube...")
            time.sleep(15)
        
        # 2. Creación de nueva arquitectura
        ConsolaDelSistema.mostrar_log(f"Creando índice de ALTA FIDELIDAD '{self.index_name}' (Dims: {self.dimension})...")
        self.pc.create_index(
            name=self.index_name,
            dimension=self.dimension,
            metric=self.metric,
            spec=ServerlessSpec(
                cloud="aws", 
                region="us-east-1" # Región estándar para el Tier de Pinecone
            )
        )
        ConsolaDelSistema.mostrar_log("✅ Índice recreado exitosamente con 3072 dimensiones.")

    def inicializar_malla_cognitiva(self):
        """Registra la génesis en la Cinta, manejando resilencia ante cuotas de IA."""
        try:
            cinta = MallaCognitivaCompartida()
            cinta.inicializar_auditoria_financiera()
            
            # Registro en la Bitácora Forense
            try:
                cinta.registrar_evento_forense_detallado(
                    emisor="AGENTE_INICIALIZADOR",
                    receptor="INFRAESTRUCTURA_MEMORIA",
                    mensaje=f"Génesis Vectorial: Índice {self.index_name} elevado a {self.dimension} dims."
                )
            except Exception:
                ConsolaDelSistema.mostrar_log("⚠️ Nota: Registro en IA omitido (Cuota), pero la Cinta está activa.")
            
            cinta.guardar_instantanea_en_disco()
            ConsolaDelSistema.mostrar_log("🧠 Malla Cognitiva sincronizada localmente.")
            return cinta
        except Exception as e:
            ConsolaDelSistema.mostrar_log(f"⚠️ Advertencia al inicializar Cinta: {e}")

    def ejecutar_workflow_genesis(self):
        """Dispara el proceso de preparación para la V7.0."""
        print("\n" + "="*75)
        print("🚀 SYMBIOMEMESIS v7.0 - GÉNESIS DE INFRAESTRUCTURA DE ALTA FIDELIDAD")
        print("="*75)
        
        try:
            self.purgar_y_recrear_indice()
            self.inicializar_malla_cognitiva()
            print(f"\n✅ INFRAESTRUCTURA VECTORIAL LISTA PARA {self.dimension} DIMENSIONES")
            print("="*75 + "\n")
        except Exception as e:
            print(f"\n❌ FALLO CRÍTICO EN GÉNESIS: {str(e)}")

if __name__ == "__main__":
    agente = AgenteInicializadorMemoriaV7()
    agente.ejecutar_workflow_genesis()