"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.1 - UNIVERSIDAD DEL ROSARIO
MODULO: fis_telemetria_v8.py (Centro de Auditoría Forense y Trazabilidad)
UBICACIÓN: /FIS_VERSION8/
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Sistema de registro de Caja Blanca. Captura:
    1. Metas-Datos: Tokens (Input/Output), Costo USD, Latencia.
    2. Lógica Agéntica: Input -> CoT -> Output.
    3. Explicabilidad Matemática: Desglose de fórmulas y cálculos dU/dt.
    4. Persistencia: Logs, Cinta Vectorial y Bitácora para Streamlit.
=============================================================================
"""

import os
import sys
import time
import logging
import pandas as pd
from datetime import datetime
from contextlib import contextmanager
from typing import Optional, List, Dict, Any

# --- CONFIGURACIÓN DE COSTOS (REFERENCIA MARZO 2026) ---
PRECIOS_TOKENS = {
    "gpt-4o": {"input": 2.50 / 1_000_000, "output": 10.00 / 1_000_000}, # USD por token
    "gemini-2.0-flash": {"input": 0.10 / 1_000_000, "output": 0.40 / 1_000_000}
}

class ColoresUR_v8:
    RESET = "\033[0m"
    NEGRITA = "\033[1m"
    VINO = "\033[31m"
    AZUL_SIS = "\033[34m"
    VERDE_AG = "\033[32m"
    AMARILLO_HITL = "\033[33m"
    CIAN_FIN = "\033[36m"
    GRIS_META = "\033[90m"

# --- DIRECTORIOS DE LOGS ---
LOGS_DIR = os.path.join(os.path.dirname(__file__), "LOGS_v8")
os.makedirs(LOGS_DIR, exist_ok=True)
log_filename = os.path.join(LOGS_DIR, f"auditoria_forense_v8_{datetime.now().strftime('%Y%m%d')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(message)s',
    handlers=[logging.FileHandler(log_filename, encoding='utf-8')]
)
logger = logging.getLogger("AUDITORIA_V8")

# =============================================================================
# 🧠 RASTREADOR DE TAPEAGENTS V8 (ECONOMETRÍA Y LÓGICA)
# =============================================================================
class RegistroAuditoriaAgente:
    """Estructura de datos para un paso en la Cinta de Auditoría."""
    def __init__(self, agente: str, modelo: str):
        self.agente = agente
        self.modelo = modelo
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.hora = datetime.now().strftime("%H:%M:%S")
        self.input_text = ""
        self.cot_text = "N/A"
        self.output_text = ""
        self.tokens_in = 0
        self.tokens_out = 0
        self.costo_usd = 0.0
        self.pasos_matematicos = []
        self.latencia = 0.0
        self.status = "OK"
        self.vector_id = "PENDING"

    def calcular_costo(self):
        """Calcula el impacto económico basado en el modelo utilizado."""
        precios = PRECIOS_TOKENS.get(self.modelo, PRECIOS_TOKENS["gemini-2.0-flash"])
        self.costo_usd = (self.tokens_in * precios["input"]) + (self.tokens_out * precios["output"])

    def registrar_tokens(self, tokens_in: int, tokens_out: int):
        """
        FIX V8.1: Proporciona el método esperado por los Agentes Tester y ABC 
        para evitar errores de atributo.
        """
        self.tokens_in = tokens_in
        self.tokens_out = tokens_out
        self.calcular_costo()

# =============================================================================
# 🏫 TELEMETRÍA MAESTRA V8 (HUB DE CAJA BLANCA)
# =============================================================================
class TelemetriaMaestraV8:
    bitacora_forense: List[RegistroAuditoriaAgente] = []

    @staticmethod
    def encabezado(titulo: str):
        banner = f"\n{ColoresUR_v8.NEGRITA}{ColoresUR_v8.AZUL_SIS}{'═'*80}\n🧬 {titulo.center(76)}\n{'═'*80}{ColoresUR_v8.RESET}"
        print(banner)
        logger.info(f"=== FASE: {titulo} ===")

    @staticmethod
    def error(msg: str):
        print(f"{ColoresUR_v8.VINO}{ColoresUR_v8.NEGRITA}[❌ ERROR]{ColoresUR_v8.RESET} {msg}")
        logger.error(msg)

    @contextmanager
    @staticmethod
    def monitor_agente(cinta, agente: str, modelo: str, tarea: str):
        """
        Monitor avanzado para TapeAgents. 
        Captura el ciclo completo: Input -> CoT -> Output -> Costo -> Math.
        """
        inicio = time.time()
        registro = RegistroAuditoriaAgente(agente, modelo)
        registro.input_text = tarea
        
        print(f"{ColoresUR_v8.VERDE_AG}[{agente}]{ColoresUR_v8.RESET} activado con {modelo}...")

        try:
            yield registro
        except Exception as e:
            registro.status = "ERROR"
            TelemetriaMaestraV8.error(f"Excepción en {agente}: {str(e)}")
            raise e
        finally:
            registro.latencia = time.time() - inicio
            registro.calcular_costo()
            
            # Persistencia en Memoria para UI y Portal
            TelemetriaMaestraV8.bitacora_forense.append(registro)
            
            # Log de Consola Estilo Caja Blanca
            print(f"      {ColoresUR_v8.GRIS_META}└─ 🎫 Tokens: {registro.tokens_in + registro.tokens_out} | 💸 Costo: ${registro.costo_usd:.6f} USD{ColoresUR_v8.RESET}")
            if registro.pasos_matematicos:
                print(f"      {ColoresUR_v8.CIAN_FIN}Σ Operaciones Matematicas:{ColoresUR_v8.RESET}")
                for paso in registro.pasos_matematicos:
                    print(f"         {ColoresUR_v8.CIAN_FIN}→ {paso}{ColoresUR_v8.RESET}")

            # Sincronización con la Cinta v8
            try:
                cinta.registrar_evento_forense_detallado(
                    emisor=agente,
                    receptor="CINTA_V8",
                    mensaje=f"Ejecución de {agente} finalizada.",
                    entrada=registro.input_text,
                    salida=registro.output_text,
                    status=registro.status,
                    tokens=registro.tokens_in + registro.tokens_out,
                    costo=registro.costo_usd,
                    desglose_math=registro.pasos_matematicos
                )
                # Actualizamos el vector_id en el registro para el informe PDF
                if hasattr(cinta, 'bitacora_forense') and cinta.bitacora_forense:
                    registro.vector_id = cinta.bitacora_forense[-1].vector_id
            except Exception as e:
                logger.warning(f"Error sincronizando cinta vectorial: {e}")

    @staticmethod
    def explicar_calculo(agente_registro: RegistroAuditoriaAgente, formula: str, variables: Dict[str, Any], resultado: Any):
        """
        Método especializado para inyectar trazabilidad matemática en el log.
        """
        explicacion = f"Fórmula: {formula} | Variables: {variables} | Resultado: {resultado}"
        agente_registro.pasos_matematicos.append(explicacion)
        logger.info(f"[MATH] {explicacion}")

    @staticmethod
    def obtener_resumen_economico() -> Dict[str, float]:
        """Calcula el gasto acumulado de la sesión."""
        total_usd = sum(r.costo_usd for r in TelemetriaMaestraV8.bitacora_forense)
        total_tokens = sum(r.tokens_in + r.tokens_out for r in TelemetriaMaestraV8.bitacora_forense)
        return {"total_usd": total_usd, "total_tokens": total_tokens}

    @staticmethod
    def evento(agente: str, accion: str, color=ColoresUR_v8.VERDE_AG):
        """Marca un hito simple en la auditoría."""
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"{color}[{agente}]{ColoresUR_v8.RESET} -> {accion} | {ts}")
        logger.info(f"[{agente}] {accion}")