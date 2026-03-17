"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.1 - UNIVERSIDAD DEL ROSARIO
MODULO: Orquestador Maestro (Backend de Consola / Motor de Ejecución)
UBICACIÓN: /FIS_VERSION8/
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Motor de ejecución puro para terminal. 
    1. Ejecución secuencial del enjambre (Génesis -> ABC -> Tester -> U).
    2. Persistencia en Cinta Pydantic y Pinecone (3072 dims).
    3. Desacoplado de Streamlit para pruebas de rendimiento y estabilidad.
=============================================================================
"""

import os
import sys
import time
from typing import Optional

# --- CARGA DE ENTORNO Y DEPENDENCIAS ---
from dotenv import load_dotenv
load_dotenv()

try:
    from fis_telemetria_v8 import TelemetriaMaestraV8 as TM, ColoresUR_v8
    from fis_fabrica_agentes_v8 import FabricaAgentesV8
    from fis_cintagentica_v8 import MallaCognitivaCompartidaV8
except ImportError as e:
    print(f"❌ Error Crítico de Dependencias: {e}")
    sys.exit(1)

# =============================================================================
# 🛡️ CLASE DE CONTROL DE MISIÓN (BACKEND)
# =============================================================================
class MotorSymbiomemesisV8:
    """
    Controlador de la lógica de negocio. Ejecuta el enjambre de agentes
    asegurando la trazabilidad de Caja Blanca.
    """

    def __init__(self, id_proyecto: str = "AUDITORIA_TERMINAL_V8"):
        self.cinta = MallaCognitivaCompartidaV8()
        self.cinta.identificador_proyecto = id_proyecto
        self.cinta.inicializar_auditoria_v8()

    def ejecutar_pipeline_completo(self, facultad: str, programa: str):
        """Ejecuta todas las fases del enjambre de forma determinista."""
        TM.encabezado(f"INICIANDO MOTOR V8.1 - PROYECTO: {self.cinta.identificador_proyecto}")
        
        try:
            # --- FASE 1: GÉNESIS DE DATOS ---
            TM.evento("ORQUESTADOR", "Activando Agente Génesis para creación de Arsenal...")
            agente_gen = FabricaAgentesV8.crear_agente_genesis()
            res_gen = agente_gen.ejecutar(
                self.cinta, 
                f"Generar datos para {programa} en {facultad}",
                facultad_sel=[facultad]
            )
            TM.evento("SISTEMA", f"Resultado Génesis: {res_gen}")

            # --- FASE 2: LIQUIDACIÓN ABC ---
            TM.evento("ORQUESTADOR", "Iniciando Motor ABC para costeo de unidad mínima (Clase)...")
            agente_abc = FabricaAgentesV8.crear_agente_abc()
            res_abc = agente_abc.ejecutar(self.cinta, "Ejecutar liquidación por registro de clase")
            TM.evento("SISTEMA", f"Resultado ABC: {res_abc}")

            # --- FASE 3: TESTER ESTOCÁSTICO ---
            TM.evento("ORQUESTADOR", "Activando Agente Tester para valoración de 45 indicadores...")
            agente_tst = FabricaAgentesV8.crear_agente_tester()
            res_tst = agente_tst.ejecutar(self.cinta, "Realizar medición M1 de la Malla de Tesis", iteracion=1)
            TM.evento("SISTEMA", f"Resultado Tester: {res_tst}")

            # --- FASE 4: RESOLUCIÓN MATEMÁTICA U ---
            TM.evento("ORQUESTADOR", "Calculando Utilidad Simbiótica Escalar U...")
            agente_u = FabricaAgentesV8.crear_agente_matematico_u()
            res_u = agente_u.ejecutar(self.cinta, "Resolver ecuación de bienestar simbiótico")
            TM.evento("SISTEMA", f"Resultado U: {res_u}")

            # --- FASE 5: ANÁLISIS DE GRADIENTE ---
            TM.evento("ORQUESTADOR", "Analizando razón de cambio dU/dM...")
            agente_grad = FabricaAgentesV8.crear_agente_gradiente_razonador()
            res_grad = agente_grad.ejecutar(self.cinta, "Determinar convergencia del sistema")
            TM.evento("SISTEMA", f"Resultado Gradiente: {res_grad}")

            # CIERRE EXITOSO
            self._mostrar_resumen_final()

        except Exception as e:
            TM.error(f"Falla crítica en el pipeline: {str(e)}")
            self.cinta.error_actual = {"msg": str(e), "ts": time.time()}

    def _mostrar_resumen_final(self):
        """Muestra la telemetría económica final en consola."""
        resumen = TM.obtener_resumen_economico()
        u_final = self.cinta.datos_matriz_auditoria.get('valor_u', 0.0)
        
        print(f"\n{ColoresUR_v8.NEGRITA}{'═'*80}")
        print(f"📊 RESUMEN FINAL DE AUDITORÍA V8.1")
        print(f"{'═'*80}{ColoresUR_v8.RESET}")
        print(f"✅ UTILIDAD U: {u_final:.6f}")
        print(f"💸 GASTO TOTAL: ${resumen['total_usd']:.5f} USD")
        print(f"🎫 TOKENS: {resumen['total_tokens']:,}")
        print(f"📂 CINTA PERSISTIDA EN: LOGS_v8/cinta_v8_checkpoint.json")
        print(f"{'═'*80}\n")

# =============================================================================
# 🚀 PUNTO DE ENTRADA (VS CODE TERMINAL)
# =============================================================================
if __name__ == "__main__":
    # Parámetros de inducción por defecto
    FACULTAD_OBJETIVO = "ESCUELA DE INGENIERÍA, CIENCIA Y TECNOLOGÍA"
    PROGRAMA_OBJETIVO = "DOCTORADO EN INGENIERÍA, CIENCIA Y TECNOLOGÍA"

    motor = MotorSymbiomemesisV8(id_proyecto="AUDITORIA_DOCTORAL_FREDY")
    motor.ejecutar_pipeline_completo(FACULTAD_OBJETIVO, PROGRAMA_OBJETIVO)