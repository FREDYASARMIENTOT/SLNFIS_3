"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.1 - UNIVERSIDAD DEL ROSARIO
MODULO: Fábrica de Agentes Tape-Centric (v8.1)
UBICACIÓN: /FIS_VERSION8/
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Implementa la arquitectura TapeAgents de ServiceNow.
    FIX ESTRUCTURAL: Importaciones estándar al inicio del archivo. 
    Se eliminan los import circulares y los problemas de pathing en Streamlit.
=============================================================================
"""

import os
import sys
import time
from datetime import datetime
from typing import List, Dict, Optional, Any, Callable
from pydantic import BaseModel, ConfigDict, Field
from google import genai
from dotenv import load_dotenv

# --- CARGA DE CONFIGURACIÓN ---
load_dotenv()

# --- AGREGAR RUTA DEL PROYECTO AL PATH DE PYTHON ---
# Esto garantiza que Python encuentre la carpeta FIS_VERSION8 desde cualquier lugar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- IMPORTACIONES LOCALES SEGURAS ---
try:
    from FIS_VERSION8.fis_telemetria_v8 import TelemetriaMaestraV8 as TM
    from FIS_VERSION8.fis_generador_csvs_v8 import AgenteGeneradorFisV8
    from FIS_VERSION8.fis_calculaCostosABC_v8 import MotorDeCosteoFinancieroABC_V8
    from FIS_VERSION8.fis_agenteTester_v8 import AgenteTesterv8
    from FIS_VERSION8.fis_calculaUtilidadSimbiotica_v8 import AgenteUtilidadSimbioticaV8
    from FIS_VERSION8.fis_calculaSimbiomemesis_v8 import MotorMatematicoSymbiomemesisV8
    from FIS_VERSION8.fis_chatbot_v8 import AgenteChatbotV8
except ImportError as e:
    print(f"❌ Error de Importación Inicial en Fábrica V8: {e}")
    # Fallbacks de seguridad si fallan los módulos físicos
    class TM:
        @staticmethod
        def monitor_agente(c, n, m, t): 
            from contextlib import contextmanager
            @contextmanager
            def dummy(): yield type('Obj', (), {'cot_text':'', 'output_text':'', 'registrar_tokens': lambda *a, **k: None})()
            return dummy()
        @staticmethod
        def error(msg): print(f"❌ {msg}")
    AgenteGeneradorFisV8 = MotorDeCosteoFinancieroABC_V8 = AgenteTesterv8 = AgenteUtilidadSimbioticaV8 = MotorMatematicoSymbiomemesisV8 = AgenteChatbotV8 = None

# =============================================================================
# 🧬 CLASE MAESTRA: AGENTE TAPE-CENTRIC V8.1
# =============================================================================
class AgenteSymbiomemesisV8(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    nombre: str
    rol: str
    system_prompt: str
    proveedor: str = "GOOGLE"
    modelo: str = Field(default_factory=lambda: os.getenv("MODEL_NAME", "gemini-2.5-flash"))
    es_razonador: bool = False
    herramienta: Optional[Callable] = None

    def ejecutar(self, cinta: Any, tarea_input: str, **kwargs) -> Any:
        inicio_timestamp = time.time()
        
        with TM.monitor_agente(cinta, self.nombre, self.modelo, tarea_input) as monitor:
            
            # --- 1. THOUGHT STEP ---
            pensamiento_cot = self._generar_pensamiento_cot(tarea_input)
            monitor.cot_text = pensamiento_cot 

            step_index = len(getattr(cinta, 'bitacora_forense', []))
            metadata_thought = {
                "step_index": step_index,
                "agent_metadata": {"role": self.rol, "engine": self.modelo}
            }

            # --- 2. ACTION STEP ---
            resultado = "FALLO_EJECUCION"
            status_step = "ERROR"
            try:
                if self.herramienta:
                    kwargs['monitor_forense'] = monitor 
                    resultado = self.herramienta(cinta, **kwargs)
                    status_step = "SUCCESS"
            except Exception as e:
                resultado = f"ERROR_AGENTE_V8: {str(e)}"
                status_step = "FAILED"
                TM.error(f"Falla en {self.nombre}: {e}")

            # --- 3. OBSERVATION STEP ---
            latencia = (time.time() - inicio_timestamp) * 1000
            
            lista_de_steps = [
                {"kind": "thought", "content": pensamiento_cot, "metadata": metadata_thought},
                {"kind": "action", "content": f"Ejecución de rutina en entorno Python por {self.nombre}."},
                {"kind": "observation", "content": str(resultado), "metadata": {"latency_ms": round(latencia, 2)}}
            ]

            monitor.output_text = str(resultado)
            cinta.registrar_evento_forense_detallado(
                emisor=self.nombre, 
                receptor="TAPE_AGENTS_V8",
                mensaje=f"Tarea completada: {self.rol}",
                entrada=tarea_input, 
                salida=str(resultado), 
                status=status_step,
                steps=lista_de_steps 
            )
            
            return resultado

    def _generar_pensamiento_cot(self, prompt_usuario: str) -> str:
        instruccion = (f"Eres {self.nombre}, experto {self.rol}. "
                       f"{self.system_prompt}. Explica brevemente tu estrategia para esta tarea.")
        try:
            client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
            resp = client.models.generate_content(
                model=self.modelo, 
                contents=f"{instruccion} | TAREA: {prompt_usuario}"
            )
            return resp.text
        except Exception as e:
            return f"Plan de acción por defecto (Offline): {e}"

# =============================================================================
# 🏗️ FÁBRICA DE AGENTES V8.1 (IMPORTACIONES GLOBALES SEGURAS)
# =============================================================================
class FabricaAgentesV8:
    
    @staticmethod
    def crear_agente_genesis() -> AgenteSymbiomemesisV8:
        if not AgenteGeneradorFisV8: return None
        return AgenteSymbiomemesisV8(
            nombre="AGENTE_GENESIS_V8",
            rol="Arquitecto de Datos",
            system_prompt="Construye el arsenal CSV y el consolidado Excel Maestro UR.",
            herramienta=AgenteGeneradorFisV8().ejecutar_plan_total
        )

    @staticmethod
    def crear_agente_abc() -> AgenteSymbiomemesisV8:
        if not MotorDeCosteoFinancieroABC_V8: return None
        return AgenteSymbiomemesisV8(
            nombre="AGENTE_ABC_V8",
            rol="Liquidador Financiero ABC",
            system_prompt="Calcula costos directos e indirectos por unidad mínima de Clase.",
            herramienta=MotorDeCosteoFinancieroABC_V8.ejecutar_calculo_de_costos_abc
        )

    @staticmethod
    def crear_agente_tester() -> AgenteSymbiomemesisV8:
        if not AgenteTesterv8: return None
        return AgenteSymbiomemesisV8(
            nombre="AGENTE_TESTER_V8",
            rol="Auditor Forense de Indicadores",
            system_prompt="Valora la malla de 45 indicadores y extrae las 15 variables para U.",
            herramienta=AgenteTesterv8.ejecutar_evaluacion_indicadores
        )

    @staticmethod
    def crear_agente_matematico_u() -> AgenteSymbiomemesisV8:
        if not AgenteUtilidadSimbioticaV8: return None
        return AgenteSymbiomemesisV8(
            nombre="AGENTE_CALCULO_U_V8",
            rol="Liquidador de Bienestar Simbiótico",
            system_prompt="Resuelve la ecuación escalar de utilidad simbiótica U.",
            herramienta=AgenteUtilidadSimbioticaV8.calcular_utilidad_u_puntual
        )

    @staticmethod
    def crear_agente_gradiente_razonador() -> AgenteSymbiomemesisV8:
        if not MotorMatematicoSymbiomemesisV8: return None
        return AgenteSymbiomemesisV8(
            nombre="AGENTE_GRADIENTE_V8",
            rol="Analista de Convergencia Sistémica",
            system_prompt="Analiza dU/dt y gradientes de cambio para detectar Simbiomemesis o Entropía.",
            es_razonador=True,
            herramienta=MotorMatematicoSymbiomemesisV8.analizar_gradiente_cambio
        )

    @staticmethod
    def crear_agente_chatbot_rag() -> AgenteSymbiomemesisV8:
        if not AgenteChatbotV8: return None
        return AgenteSymbiomemesisV8(
            nombre="AGENTE_CHATBOT_V8",
            rol="Consultor RAG de Caja Blanca",
            system_prompt="Interroga la Cinta, Pinecone y Logs para explicar el estado del sistema.",
            es_razonador=True,
            herramienta=AgenteChatbotV8.procesar_razonamiento
        )