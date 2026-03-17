"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v7.0 - UNIVERSIDAD DEL ROSARIO
MODULO: fis_telemetria_v7.py (Centro de Mando y Telemetría Unificada)
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Centro neurálgico de rastreo. Fusiona:
    1. Visualización ANSI (v6)
    2. Rastreo Vectorial RAG (v7)
    3. Logging Estándar de Python (.log)
    4. Gestión de la carpeta LOGS/
=============================================================================
"""

import os
import sys
import time
import logging
from datetime import datetime
from contextlib import contextmanager
from typing import Optional

# Configuración de Colores ANSI Institucionales
class ColoresUR:
    RESET = "\033[0m"
    NEGRITA = "\033[1m"
    VINO = "\033[31m"      # Simulado con Rojo en ANSI estándar
    AZUL_SIS = "\033[34m"
    VERDE_AG = "\033[32m"
    AMARILLO_HITL = "\033[33m"
    CIAN_FIN = "\033[36m"
    GRIS_META = "\033[90m"

# =============================================================================
# 📁 CONFIGURACIÓN DE LOGGING Y DIRECTORIOS
# =============================================================================
LOGS_DIR = "LOGS"
os.makedirs(LOGS_DIR, exist_ok=True)

log_filename = os.path.join(LOGS_DIR, f"symbiomemesis_v7_{datetime.now().strftime('%Y%m%d')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
# Deshabilitamos los logs estándar para que no dupliquen la salida de consola personalizada
logger = logging.getLogger("SYMBIOMEMESIS_V7")
logging.getLogger().handlers = [logging.FileHandler(log_filename, encoding='utf-8')]

# =============================================================================
# 🧠 RASTREADOR DE RECURSOS V7
# =============================================================================
class RastreadorDeConsumoV7:
    def __init__(self):
        self.tokens_entrada = 0
        self.tokens_salida = 0
        self.operaciones_vectoriales = 0
        self.latencia_vectorial_ms = 0.0
        self.exito_rag = True

    def registrar_tokens(self, entrada: int, salida: int):
        self.tokens_entrada = entrada
        self.tokens_salida = salida

    def registrar_accion_vectorial(self, latencia_ms: float, exito: bool = True):
        self.operaciones_vectoriales += 1
        self.latencia_vectorial_ms += latencia_ms
        self.exito_rag = exito

# =============================================================================
# 🏫 INTERFAZ TERMINAL Y MONITOR DE CONTEXTO
# =============================================================================
class TelemetriaMaestraV7:
    """Controlador central de la capa de presentación y auditoría."""

    @staticmethod
    def encabezado(titulo: str):
        banner = f"\n{ColoresUR.NEGRITA}{ColoresUR.AZUL_SIS}{'═'*80}\n🧬 {titulo.center(76)}\n{'═'*80}{ColoresUR.RESET}"
        print(banner)
        logger.info(f"--- INICIO FASE: {titulo} ---")

    @staticmethod
    def evento(agente: str, accion: str, color=ColoresUR.VERDE_AG):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{color}[{agente}]{ColoresUR.RESET} -> {accion} {ColoresUR.GRIS_META}| {timestamp}{ColoresUR.RESET}")
        logger.info(f"[{agente}] {accion}")

    @staticmethod
    def error(msg: str):
        print(f"\n{ColoresUR.VINO}{ColoresUR.NEGRITA}[❌ ERROR]{ColoresUR.RESET} {msg}")
        logger.error(msg)

    @staticmethod
    def info_financiera(msg: str):
        print(f"{ColoresUR.CIAN_FIN}[FINANZAS]{ColoresUR.RESET} {msg}")
        logger.info(f"[FINANZAS] {msg}")

    @contextmanager
    @staticmethod
    def monitor(cinta, agente: str, accion: str, modelo: str = "gemini-2.0"):
        """Gestor de contexto para medir la acción del agente."""
        inicio = time.time()
        rastreador = RastreadorDeConsumoV7()
        TelemetriaMaestraV7.evento(agente, f"Iniciando: {accion}")
        
        try:
            yield rastreador
        finally:
            tiempo_total = time.time() - inicio
            status_rag = "OK" if rastreador.exito_rag else "FAIL"
            
            # Formatear metadata para consola
            meta_msg = (f"⏱️ {tiempo_total:.2f}s | 🎫 Tkn: {rastreador.tokens_entrada + rastreador.tokens_salida} | "
                        f"📡 RAG: {rastreador.operaciones_vectoriales} op ({status_rag})")
            
            print(f"      {ColoresUR.GRIS_META}└─ {meta_msg}{ColoresUR.RESET}")
            
            # Persistencia en la Cinta (Caja Blanca)
            try:
                from fis_cintagentica_v7 import RegistroDeTelemetriaDeAgente
                registro = RegistroDeTelemetriaDeAgente(
                    nombre_del_agente_ejecutor=agente,
                    accion_realizada_por_agente=f"{accion} [RAG_{status_rag}]",
                    modelo_de_lenguaje_utilizado=modelo,
                    cantidad_tokens_de_entrada=rastreador.tokens_entrada,
                    cantidad_tokens_de_salida=rastreador.tokens_salida,
                    tiempo_de_ejecucion_en_segundos=tiempo_total
                )
                cinta.agregar_registro_de_telemetria(registro)
            except Exception as e:
                logger.warning(f"No se pudo inyectar telemetría en la cinta: {e}")

# =============================================================================
# 🧪 TEST DE INTEGRACIÓN
# =============================================================================
if __name__ == "__main__":
    # Mock de cinta para prueba
    class MockCinta:
        def agregar_registro_de_telemetria(self, r): pass

    TelemetriaMaestraV7.encabezado("PRUEBA DE TELEMETRÍA CENTRALIZADA V7.0")
    
    with TelemetriaMaestraV7.monitor(MockCinta(), "Agente_ABC", "Cálculo de Áreas") as m:
        time.sleep(1) # Simulación de proceso
        m.registrar_tokens(150, 250)
        m.registrar_accion_vectorial(45.5)
        TelemetriaMaestraV7.info_financiera("TRM consultada exitosamente.")
        
    TelemetriaMaestraV7.evento("SISTEMA", "Proceso finalizado.", ColoresUR.AZUL_SIS)