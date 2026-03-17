"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v7.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Malla Cognitiva Compartida (La Cinta) - Hub de Telemetría Total
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Define la estructura estigmérgica para auditoría de Caja Blanca. 
    Asegura integridad de objetos Pydantic, soporte para 3072 dimensiones
    y compatibilidad total con el generador de informes PDF.
=============================================================================
"""

import os
import sys
import json
from datetime import datetime
from typing import List, Dict, Optional, Any, Set
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# --- MOTORES DE IA Y VECTORIALES ---
from google import genai
from pinecone import Pinecone

# --- INTEGRACIÓN CON TELEMETRÍA CENTRALIZADA ---
try:
    from fis_telemetria_v7 import TelemetriaMaestraV7 as TM, ColoresUR
except ImportError:
    class TM:
        @staticmethod
        def evento(a, m, **k): print(f"[{a}] {m}")
        @staticmethod
        def error(m): print(f"[ERROR] {m}")

load_dotenv()

# =============================================================================
# 🔐 CONFIGURACIÓN DE INFRAESTRUCTURA (3072 DIMS)
# =============================================================================
try:
    google_key = os.getenv("GOOGLE_API_KEY")
    pinecone_key = os.getenv("PINECONE_API_KEY")
    pc = Pinecone(api_key=pinecone_key)
    # Referencia al índice de alta fidelidad (3072 dims)
    indice_pinecone = pc.Index(os.getenv("PINECONE_INDEX", "symbiomemesis-v7-index"))
    client_gemini = genai.Client(api_key=google_key)
except Exception as e:
    TM.error(f"Falla de Infraestructura Vectorial: {e}")

# =============================================================================
# 📊 MODELOS DE DATOS (AUDITORÍA FORENSE)
# =============================================================================

class RegistroForenseDetallado(BaseModel):
    """
    Estructura atómica de un evento. 
    Usa BaseModel para asegurar que el reporteador siempre reciba objetos.
    """
    marca_de_tiempo: str
    fecha: str
    hora: str
    emisor: str
    receptor: str
    mensaje_accion: str
    entrada_cruda: str
    salida_cruda: str
    vector_id: str
    status: str = "OK"
    detalles_extra: Optional[Dict[str, Any]] = None

class RegistroInteraccionChatbot(BaseModel):
    id_sesion: str = Field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M"))
    fecha_hora: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    user_prompt: str
    ai_response: str
    intent: str
    tokens: int = 0
    latencia_ms: float = 0.0

class ResultadosDelInstrumentoDelTester(BaseModel):
    valores_crudos_cuarenta_y_cinco_indicadores: Dict[str, List[float]] = Field(default_factory=dict)
    numero_de_iteracion_actual: int = 0

class ReporteFinancieroCosteoDeClase(BaseModel):
    costo_total_calculado: float
    desglose_de_costos_por_categoria: Dict[str, float]

class MatrizDeAuditoriaCientifica(BaseModel):
    variables_promediadas_por_momento: Dict[str, float]
    valor_precalculo_de_friccion: float
    observaciones_cualitativas_del_auditor: str
    desarrollo_matematico_paso_a_paso: List[str]

# =============================================================================
# 🧠 MALLA COGNITIVA COMPARTIDA (LA CINTA)
# =============================================================================
class MallaCognitivaCompartida(BaseModel):
    identificador_proyecto: str = "Tesis_Fredy_Sarmiento_V7"
    etapa_actual: str = "ETAPA_GENESIS"
    
    # Registros de la Malla
    bitacora_conversacional: List[RegistroInteraccionChatbot] = Field(default_factory=list)
    bitacora_forense: List[RegistroForenseDetallado] = Field(default_factory=list)
    
    # Objetos de Estado
    datos_reporte_financiero: Optional[ReporteFinancieroCosteoDeClase] = None
    datos_resultados_tester: Optional[ResultadosDelInstrumentoDelTester] = None
    datos_matriz_auditoria: Optional[MatrizDeAuditoriaCientifica] = None

    # --- MÉTODOS DE GESTIÓN DE ETAPAS ---
    def cambiar_etapa_del_enjambre(self, nueva_etapa: str, agente: str):
        etapa_anterior = self.etapa_actual
        self.etapa_actual = nueva_etapa
        msg = f"Cambio de estado: {etapa_anterior} ➔ {nueva_etapa}"
        self.registrar_evento_forense_detallado(
            emisor=agente, receptor="SISTEMA_CENTRAL",
            mensaje=msg, entrada=etapa_anterior, salida=nueva_etapa
        )

    # --- MÉTODO MAESTRO: REGISTRO FORENSE CON BLINDAJE ---
    def registrar_evento_forense_detallado(self, emisor: str, receptor: str, mensaje: str, 
                                           entrada: str = "N/A", salida: str = "N/A", 
                                           status: str = "OK", **kwargs):
        """
        Persistencia Vectorial (3072 dims) y Local. 
        Garantiza 'marca_de_tiempo' y compatibilidad con alias 'resultado'.
        """
        ahora = datetime.now()
        ts_full = ahora.strftime("%Y-%m-%d %H:%M:%S")
        v_id = f"v_{ahora.strftime('%y%m%d_%H%M%S_%f')}"
        
        # Resolución de alias para compatibilidad (evita error de parámetro inesperado)
        final_salida = salida if salida != "N/A" else str(kwargs.get('resultado', "N/A"))

        # 1. Persistencia Vectorial
        try:
            res = client_gemini.models.embed_content(
                model="gemini-embedding-2-preview",
                contents=f"[{self.etapa_actual}] {emisor} -> {mensaje}: {final_salida}"
            )
            indice_pinecone.upsert(vectors=[{
                "id": v_id, 
                "values": res.embeddings[0].values,
                "metadata": {"emisor": emisor, "etapa": self.etapa_actual}
            }], namespace="auditoria-v7")
        except Exception:
            v_id = "LOCAL_ONLY"
            status = "WARN_VECTOR_FAIL"

        # 2. Creación del objeto Pydantic
        nuevo_reg = RegistroForenseDetallado(
            marca_de_tiempo=ts_full,
            fecha=ahora.strftime("%Y-%m-%d"),
            hora=ahora.strftime("%H:%M:%S"),
            emisor=emisor,
            receptor=receptor,
            mensaje_accion=mensaje,
            entrada_cruda=str(entrada),
            salida_cruda=str(final_salida),
            vector_id=v_id,
            status=status,
            detalles_extra=kwargs if kwargs else None
        )
        self.bitacora_forense.append(nuevo_reg)
        self.guardar_instantanea_en_disco()

    # =========================================================================
    # 🤖 MÉTODOS DE CONSULTA (RESOLUCIÓN DE ERRORES DE UI)
    # =========================================================================

    def obtener_agentes_participantes(self) -> List[str]:
        """Extrae la lista única de agentes (Evita AttributeError en Orquestador)."""
        agentes = {reg.emisor for reg in self.bitacora_forense}
        if not agentes:
            return ["SISTEMA_CENTRAL", "LA_CINTA"]
        return sorted(list(agentes))

    def obtener_diagnostico_etapa(self) -> str:
        iconos = {
            "ETAPA_GENESIS": "⚙️", "ETAPA_COSTEO_ABC": "💰", 
            "ETAPA_TESTER_INDICADORES": "🧪", "ETAPA_RESOLUCION_MATEMATICA": "🧮",
            "ETAPA_FINALIZACION": "📄"
        }
        icono = iconos.get(self.etapa_actual, "📍")
        return f"{icono} **Etapa Actual:** `{self.etapa_actual}`"

    def obtener_log_telemetria_detallado(self) -> List[Dict[str, Any]]:
        log_data = []
        for reg in reversed(self.bitacora_forense):
            log_data.append({
                "Hora": reg.hora,
                "Agente": reg.emisor,
                "Acción": reg.mensaje_accion,
                "Status": reg.status,
                "Vector_ID": reg.vector_id[:12]
            })
        return log_data

    # --- PERSISTENCIA ---
    def guardar_instantanea_en_disco(self, ruta="LOGS/cinta_v7_master.json"):
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(self.model_dump_json(indent=4))
        except Exception as e:
            TM.error(f"Fallo guardando Cinta: {e}")

    def inicializar_auditoria_financiera(self):
        self.registrar_evento_forense_detallado(
            emisor="SISTEMA_CENTRAL", receptor="LA_CINTA",
            mensaje="Malla Cognitiva Sincronizada V7.6 - Operativa"
        )