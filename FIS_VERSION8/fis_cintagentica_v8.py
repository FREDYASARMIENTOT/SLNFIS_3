"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.1 - UNIVERSIDAD DEL ROSARIO
MODULO: Malla Cognitiva Compartida (La Cinta v8.1 - TapeAgents Edition)
UBICACIÓN: /FIS_VERSION8/
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Cinta Estigmérgica.
    FIX: Restauración de los modelos de datos (ReporteFinancieroV8) y 
    declaración de 'error_actual' para evitar crasheos de NoneType en ABC y U.
=============================================================================
"""

import os
import sys
import json
from datetime import datetime
from typing import List, Dict, Optional, Any, Set
from pydantic import BaseModel, Field, ConfigDict
from dotenv import load_dotenv

from google import genai
from pinecone import Pinecone

# --- INTEGRACIÓN CON TELEMETRÍA V8 ---
try:
    from FIS_VERSION8.fis_telemetria_v8 import TelemetriaMaestraV8 as TM
except ImportError:
    class TM:
        @staticmethod
        def evento(a, m, **k): print(f"[{a}] {m}")
        @staticmethod
        def error(m): print(f"[ERROR] {m}")

load_dotenv()

# =============================================================================
# 🔐 CONFIGURACIÓN VECTORIAL
# =============================================================================
try:
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    indice_v8 = pc.Index(os.getenv("PINECONE_INDEX", "symbiomemesis-v7-index"))
    client_gemini = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
except Exception as e:
    TM.error(f"Falla de Infraestructura Vectorial v8: {e}")

# =============================================================================
# 📊 SUB-MODELOS DE DATOS (RESTAURADOS PARA EVITAR ERRORES NoneType)
# =============================================================================
class ReporteFinancieroV8(BaseModel):
    costo_total_calculado: float = 0.0
    desglose_de_costos_por_categoria: Dict[str, Any] = Field(default_factory=dict)
    ruta_excel_auditado: str = ""

class ResultadosDelTesterV8(BaseModel):
    iteracion: int = 0
    malla_45_completa: Dict[str, float] = Field(default_factory=dict)
    variables_15_utilidad: Dict[str, float] = Field(default_factory=dict)
    status: str = "PENDING"
    timestamp: str = ""

class TapeStepV8(BaseModel):
    step_id: str
    kind: str
    emisor: str
    contenido: Any
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))

class RegistroForenseV8(BaseModel):
    marca_de_tiempo: str
    emisor: str
    receptor: str
    mensaje_accion: str
    entrada_cruda: str
    salida_cruda: str
    vector_id: str
    status: str = "OK"
    tape_steps: List[TapeStepV8] = Field(default_factory=list)
    metadata_economica: Optional[Dict[str, Any]] = None

# =============================================================================
# 🧠 MALLA COGNITIVA COMPARTIDA (LA CINTA V8.1)
# =============================================================================
class MallaCognitivaCompartidaV8(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    identificador_proyecto: str = "Symbiomemesis_v8_UR"
    etapa_actual: str = "ETAPA_SIMBIOMEMESIS"
    
    bitacora_forense: List[RegistroForenseV8] = Field(default_factory=list)
    bitacora_conversacional: List[Dict[str, str]] = Field(default_factory=list)
    
    # --- FIX: INICIALIZACIÓN DE CLASES POR DEFECTO ---
    datos_reporte_financiero: ReporteFinancieroV8 = Field(default_factory=ReporteFinancieroV8)
    datos_resultados_tester: ResultadosDelTesterV8 = Field(default_factory=ResultadosDelTesterV8)
    datos_matriz_auditoria: Dict[str, Any] = Field(default_factory=dict)
    
    # --- FIX: DECLARACIÓN EXPLÍCITA DEL CAMPO DE ERROR ---
    error_actual: Optional[Dict[str, Any]] = None

    def _sanitizar_profundamente(self, obj: Any) -> Any:
        if isinstance(obj, BaseModel):
            return {str(k): self._sanitizar_profundamente(v) for k, v in obj.__dict__.items()}
        elif isinstance(obj, dict) or "mappingproxy" in str(type(obj)):
            return {str(k): self._sanitizar_profundamente(v) for k, v in dict(obj).items()}
        elif isinstance(obj, (list, tuple, set)):
            return [self._sanitizar_profundamente(i) for i in obj]
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        else:
            return str(obj)

    def registrar_evento_forense_detallado(self, emisor: str, receptor: str, mensaje: str, 
                                           entrada: str = "N/A", salida: str = "N/A", 
                                           status: str = "OK", steps: List[Dict] = None, **kwargs):
        ahora = datetime.now()
        ts_full = ahora.strftime("%Y-%m-%d %H:%M:%S")
        v_id = f"v8_{ahora.strftime('%y%m%d_%H%M%S_%f')}"
        
        try:
            contenido_vectorial = f"[{self.etapa_actual}] {emisor} -> {mensaje} | Res: {salida[:300]}"
            res = client_gemini.models.embed_content(
                model="text-embedding-004",
                contents=contenido_vectorial
            )
            indice_v8.upsert(vectors=[{
                "id": v_id, 
                "values": res.embeddings[0].values,
                "metadata": {"emisor": emisor, "etapa": self.etapa_actual}
            }], namespace="auditoria-v8-forense")
        except:
            v_id = "VEC_OFFLINE"
            status = "WARN_LOCAL_ONLY"

        lista_steps = []
        if steps:
            for i, s in enumerate(steps):
                lista_steps.append(TapeStepV8(
                    step_id=f"{v_id}_s{i}",
                    kind=s.get('kind', 'thought'),
                    emisor=emisor,
                    contenido=s.get('content', ''),
                    metadata=self._sanitizar_profundamente(s.get('metadata', {}))
                ))

        nuevo_reg = RegistroForenseV8(
            marca_de_tiempo=ts_full,
            emisor=emisor,
            receptor=receptor,
            mensaje_accion=mensaje,
            entrada_cruda=str(entrada),
            salida_cruda=str(salida),
            vector_id=v_id,
            status=status,
            tape_steps=lista_steps,
            metadata_economica=self._sanitizar_profundamente(kwargs) if kwargs else None
        )
        self.bitacora_forense.append(nuevo_reg)
        self.guardar_estado_v8()

    def guardar_estado_v8(self, ruta="LOGS_v8/cinta_v8_checkpoint.json"):
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        try:
            data_limpia = self._sanitizar_profundamente(self)
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(data_limpia, f, indent=4, ensure_ascii=False)
        except Exception as e:
            TM.error(f"Falla persistencia Tape v8: {e}")

    def obtener_agentes_participantes(self) -> List[str]:
        agentes = {reg.emisor for reg in self.bitacora_forense if hasattr(reg, 'emisor')}
        return sorted(list(agentes)) if agentes else ["ORQUESTADOR_V8"]

    def inicializar_auditoria_v8(self):
        self.registrar_evento_forense_detallado(
            emisor="SISTEMA_V8", receptor="LA_CINTA",
            mensaje="Iniciando Tape Forense v8.1 - Arquitectura TapeAgents"
        )