"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.1 - UNIVERSIDAD DEL ROSARIO
MODULO: Fábrica de Agentes Tape-Centric (v8.1 - Blindada)
UBICACIÓN: /FIS_VERSION8/
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Orquestador de identidades agénticas v8.1. 
    Implementa el estándar TapeAgents: Thought -> Action -> Observation.
    Unifica el ecosistema en Google Gemini 2.0 Flash y text-embedding-004.
=============================================================================
"""

import os
import sys
import time
import json
from datetime import datetime
from typing import List, Dict, Optional, Any, Callable
from pydantic import BaseModel, ConfigDict
from google import genai
from dotenv import load_dotenv

# --- CARGA DE CONFIGURACIÓN ---
load_dotenv()

# --- INTEGRACIÓN CON TELEMETRÍA V8.1 ---
try:
    from FIS_VERSION8.fis_telemetria_v8 import TelemetriaMaestraV8 as TM
except ImportError:
    class TM:
        @staticmethod
        def monitor_agente(c, n, m, t): 
            # Fallback en caso de que el monitor no esté disponible
            from contextlib import contextmanager
            @contextmanager
            def dummy(): yield type('Obj', (), {'cot_text':'', 'output_text':'', 'registrar_tokens': lambda *a, **k: None})()
            return dummy()
        @staticmethod
        def error(m): print(f"[ERROR] {m}")

# =============================================================================
# 🧬 CLASE MAESTRA: AGENTE TAPE-CENTRIC V8.1
# =============================================================================
class AgenteSymbiomemesisV8(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    nombre: str
    rol: str
    system_prompt: str
    proveedor: str = "GOOGLE"
    modelo: str = "gemini-2.0-flash"
    es_razonador: bool = False
    herramienta: Optional[Callable] = None

    def ejecutar(self, cinta: Any, tarea_input: str, **kwargs) -> Any:
        """
        Ciclo de Vida inspirado en TapeAgents:
        1. THOUGHT STEP: Genera el razonamiento (CoT).
        2. ACTION STEP: Ejecuta la herramienta técnica (Módulo Python).
        3. OBSERVATION STEP: Registra el resultado con metadatos de cinta.
        """
        inicio_ms = time.time() * 1000
        
        with TM.monitor_agente(cinta, self.nombre, self.modelo, tarea_input) as monitor:
            
            # --- STEP 1: THOUGHT (Razonamiento) ---
            pensamiento_cot = self._generar_pensamiento_cot(tarea_input)
            monitor.cot_text = pensamiento_cot 

            # Metadatos del Paso (Tape Metadata)
            step_index = len(getattr(cinta, 'bitacora_forense', []))
            metadata_paso = {
                "tape_step_index": step_index,
                "agent_identity": {"name": self.nombre, "role": self.rol},
                "timestamp_start": inicio_ms
            }

            # --- STEP 2: ACTION (Ejecución) ---
            resultado = "FALLO_EJECUCION"
            status_final = "ERROR"
            
            if self.herramienta:
                try:
                    # Inyectamos el monitor para trazabilidad interna
                    kwargs['monitor_forense'] = monitor 
                    resultado = self.herramienta(cinta, **kwargs)
                    status_final = "SUCCESS"
                except Exception as e:
                    resultado = f"ERROR_AGENTE_V8: {str(e)}"
                    TM.error(f"Falla técnica en {self.nombre}: {e}")

            # --- STEP 3: OBSERVATION (Persistencia en Cinta) ---
            latencia = (time.time() * 1000) - inicio_ms
            monitor.output_text = str(resultado)
            
            # Registro en la Cinta Vectorial (Tape Persistence)
            cinta.registrar_evento_forense_detallado(
                emisor=self.nombre, 
                receptor="TAPE_AGENTS_V8",
                mensaje=f"Tarea completada: {self.rol}",
                entrada=tarea_input, 
                salida=str(resultado), 
                status=status_final,
                steps=[
                    {"kind": "thought", "content": pensamiento_cot},
                    {"kind": "action", "content": f"Ejecución {self.nombre}", "metadata": metadata_paso},
                    {"kind": "observation", "content": str(resultado), "metadata": {"latency_ms": latencia}}
                ]
            )
            
            return resultado

    def _generar_pensamiento_cot(self, prompt_usuario: str) -> str:
        """Invocación a Gemini para generar el plan de acción (Thought)."""
        instruccion = (f"Eres {self.nombre}, {self.rol}. {self.system_prompt}. "
                       f"Explica brevemente tu razonamiento para resolver la siguiente tarea.")
        try:
            client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
            resp = client.models.generate_content(
                model=self.modelo, 
                contents=f"{instruccion}\n\nTAREA: {prompt_usuario}"
            )
            return resp.text
        except Exception as e:
            return f"Razonamiento local (Offline): {e}"

# =============================================================================
# 🏗️ FÁBRICA DE AGENTES V8.1 (CON SOPORTE PARA TAPEAGENTS)
# =============================================================================
class FabricaAgentesV8:
    
    @staticmethod
    def crear_agente_genesis() -> AgenteSymbiomemesisV8:
        from FIS_VERSION8.fis_generador_csvs_v8 import AgenteGeneradorFisV8
        return AgenteSymbiomemesisV8(
            nombre="AGENTE_GENESIS_V8",
            rol="Arquitecto de Datos",
            system_prompt="Construye el arsenal CSV y el consolidado Excel Maestro UR.",
            herramienta=AgenteGeneradorFisV8().ejecutar_plan_total
        )

    @staticmethod
    def crear_agente_abc() -> AgenteSymbiomemesisV8:
        from FIS_VERSION8.fis_calculaCostosABC_v8 import MotorDeCosteoFinancieroABC_V8
        return AgenteSymbiomemesisV8(
            nombre="AGENTE_ABC_V8",
            rol="Liquidador Financiero ABC",
            system_prompt="Calcula costos directos e indirectos por unidad mínima de Clase.",
            herramienta=MotorDeCosteoFinancieroABC_V8.ejecutar_calculo_de_costos_abc
        )

    @staticmethod
    def crear_agente_tester() -> AgenteSymbiomemesisV8:
        from FIS_VERSION8.fis_agenteTester_v8 import AgenteTesterv8
        return AgenteSymbiomemesisV8(
            nombre="AGENTE_TESTER_V8",
            rol="Auditor Forense de Indicadores",
            system_prompt="Valora la malla de 45 indicadores y extrae las 15 variables para U.",
            herramienta=AgenteTesterv8.ejecutar_evaluacion_indicadores
        )

    @staticmethod
    def crear_agente_matematico_u() -> AgenteSymbiomemesisV8:
        from FIS_VERSION8.fis_calculaUtilidadSimbiotica_v8 import AgenteUtilidadSimbioticaV8
        return AgenteSymbiomemesisV8(
            nombre="AGENTE_CALCULO_U_V8",
            rol="Matemático de Utilidad Simbiótica",
            system_prompt="Resuelve la ecuación escalar de utilidad simbiótica U.",
            herramienta=AgenteUtilidadSimbioticaV8.calcular_utilidad_u_puntual
        )

    @staticmethod
    def crear_agente_gradiente_razonador() -> AgenteSymbiomemesisV8:
        from FIS_VERSION8.fis_calculaSimbiomemesis_v8 import MotorMatematicoSymbiomemesisV8
        return AgenteSymbiomemesisV8(
            nombre="AGENTE_GRADIENTE_V8",
            rol="Analista de Convergencia",
            system_prompt="Analiza dU/dt y gradientes de cambio para detectar Simbiomemesis.",
            es_razonador=True,
            herramienta=MotorMatematicoSymbiomemesisV8.analizar_gradiente_cambio
        )

    @staticmethod
    def crear_agente_chatbot_rag() -> AgenteSymbiomemesisV8:
        from FIS_VERSION8.fis_chatbot_v8 import AgenteChatbotV8
        return AgenteSymbiomemesisV8(
            nombre="AGENTE_CHATBOT_V8",
            rol="Consultor RAG de Caja Blanca",
            system_prompt="Interroga la Cinta, Pinecone y Logs para explicar el estado del sistema.",
            es_razonador=True,
            herramienta=AgenteChatbotV8.procesar_razonamiento
        )