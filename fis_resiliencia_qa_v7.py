"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v7.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Agente de Resiliencia, Calidad y QA (Self-Healing AI)
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Orquestador de resiliencia sistémica. Realiza el ciclo de vida completo 
    del enjambre en modo "Test", captura errores tipificados y genera 
    diagnósticos avanzados con LLM para garantizar la convergencia de U.
=============================================================================
"""

import os
import sys
import json
import asyncio
import traceback
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# --- IMPORTACIONES DEL ECOSISTEMA SYMBIOMEMESIS V7 ---
from fis_telemetria_v7 import TelemetriaMaestraV7 as TM, ColoresUR
from fis_cintagentica_v7 import MallaCognitivaCompartida

# Importación dinámica de agentes para el test integral
try:
    from fis_generador_csvs_v7 import AgenteGeneradorFisV7
    from fis_calculaCostosABC_V7 import MotorDeCosteoFinancieroABC_V7
    from fis_agenteTester_V7 import AgenteTesterV7
    from fis_calculaSimbiomemesis_v7 import MotorMatematicoSymbiomemesisV7
    from fis_informe_v7 import GeneradorReporteV7
except ImportError as e:
    print(f"⚠️ Advertencia de dependencias en QA: {e}")

# =============================================================================
# 🛡️ GESTIÓN DE ERRORES Y EXCEPCIONES QA
# =============================================================================
class SymbiomemesisError(Exception):
    """Clase base para errores del ecosistema."""
    def __init__(self, mensaje, codigo="ERR-QA-000", etapa="GENERAL"):
        self.codigo = codigo
        self.etapa = etapa
        super().__init__(f"[{codigo}] {mensaje}")

class FalloDeConvergenciaError(SymbiomemesisError):
    """Error cuando el sistema no logra llegar a la utilidad U."""
    pass

# =============================================================================
# 🧠 AGENTE DE RESILIENCIA V7
# =============================================================================
class AgenteResilienciaV7:
    """
    Agente de IA encargado de la auto-sanación (Self-Healing).
    Monitorea la Cinta, detecta fallos y propone reparaciones al usuario.
    """

    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.modelo_diagnostico = os.getenv("MODEL_NAME", "gpt-4o")
        self.max_reintentos = 2

    def diagnosticar_error_ia(self, etapa: str, error: Exception, tb: str) -> dict:
        """Utiliza GPT-4o para analizar el rastro forense y proponer una solución."""
        prompt = f"""
        ACTÚA COMO: Experto en Sistemas Multi-Agente y Auditoría de Software.
        CONTEXTO: Proyecto SYMBIOMEMESIS v7.0 (Universidad del Rosario).
        
        DETECCIÓN DE FALLO EN: {etapa}
        MENSAJE DE ERROR: {str(error)}
        TRACEBACK: {tb[-1200:]}
        
        TAREA:
        1. Analiza la causa raíz (¿Datos corruptos?, ¿Falta de API?, ¿Error de lógica?).
        2. Proporciona un diagnóstico amigable para el usuario del Chatbot.
        3. Proporciona una instrucción técnica precisa para el Ing. Fredy Sarmiento.
        
        FORMATO DE RESPUESTA (JSON):
        {{
            "causa_raiz": "...",
            "mensaje_chatbot": "...",
            "instruccion_tecnica": "..."
        }}
        """
        try:
            response = self.client.chat.completions.create(
                model=self.modelo_diagnostico,
                messages=[{"role": "system", "content": "Analista Senior de QA y Resiliencia."},
                          {"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception:
            return {
                "causa_raiz": "Falla en el motor de diagnóstico IA.",
                "mensaje_chatbot": "El sistema ha experimentado una anomalía no identificada.",
                "instruccion_tecnica": "Verificar logs en la carpeta /LOGS y conexión a internet."
            }

    async def ejecutar_test_de_resiliencia_completo(self, cinta: MallaCognitivaCompartida, programa_test: str):
        """
        Recorre todas las etapas del enjambre asegurando que los datos 
        fluyan correctamente por la Cinta.
        """
        TM.encabezado("SUITE DE RESILIENCIA SYMBIOMEMESIS v7.0")
        TM.evento("QA_AGENT", f"Iniciando auditoría preventiva para: {programa_test}")

        ciclo_completado = False
        reintentos = 0

        while not ciclo_completado and reintentos <= self.max_reintentos:
            etapa_actual = cinta.etapa_actual
            TM.evento("QA_AGENT", f"Validando Etapa: {etapa_actual} (Intento {reintentos + 1})")

            try:
                with TM.monitor(cinta, "QA_AGENT", f"Validacion_{etapa_actual}") as monitor:
                    
                    # --- FASE 1: ARSENAL ---
                    if etapa_actual == "ETAPA_GENESIS":
                        gen = AgenteGeneradorFisV7()
                        gen.ejecutar_plan_total(cinta, programa_solicitado=programa_test)
                        cinta.cambiar_etapa_del_enjambre("ETAPA_COSTEO_ABC", "QA_AGENT")

                    # --- FASE 2: ABC ---
                    elif etapa_actual == "ETAPA_COSTEO_ABC":
                        if MotorDeCosteoFinancieroABC_V7.ejecutar_calculo_de_costos_abc(cinta):
                            cinta.cambiar_etapa_del_enjambre("ETAPA_TESTER_INDICADORES", "QA_AGENT")
                        else:
                            raise FalloDeConvergenciaError("El motor ABC no pudo liquidar los rubros.", "ERR-QA-ABC", etapa_actual)

                    # --- FASE 3: TESTER (Variables) ---
                    elif etapa_actual == "ETAPA_TESTER_INDICADORES":
                        AgenteTesterV7.ejecutar_evaluacion_indicadores(cinta)
                        cinta.cambiar_etapa_del_enjambre("ETAPA_RESOLUCION_MATEMATICA", "QA_AGENT")

                    # --- FASE 4: MATEMÁTICA U ---
                    elif etapa_actual == "ETAPA_RESOLUCION_MATEMATICA":
                        MotorMatematicoSymbiomemesisV7.resolver_simbiomemesis_total(cinta)
                        cinta.cambiar_etapa_del_enjambre("ETAPA_FINALIZACION", "QA_AGENT")

                    # --- FASE 5: REPORTE ---
                    elif etapa_actual == "ETAPA_FINALIZACION":
                        ruta_reporte = GeneradorReporteV7.generar_pdf(cinta)
                        TM.evento("QA_AGENT", f"✅ Auditoría completada. Informe: {ruta_reporte}")
                        ciclo_completado = True

                    monitor.registrar_tokens(400, 400)
                    monitor.registrar_accion_vectorial(latencia_ms=25.0)

            except Exception as e:
                reintentos += 1
                tb = traceback.format_exc()
                diagnostico = self.diagnosticar_error_ia(etapa_actual, e, tb)
                
                # Registro Forense del Crash
                cinta.registrar_evento_forense_detallado(
                    emisor="QA_RESILIENCIA",
                    receptor="AUDITOR_FORENSE",
                    mensaje=f"CRASH EN {etapa_actual}: {diagnostico['causa_raiz']}",
                    entrada="Traceback enviado a IA",
                    salida=diagnostico['instruccion_tecnica'],
                    status="CRASH_HANDLED"
                )

                TM.error(f"Fallo detectado: {diagnostico['mensaje_chatbot']}")
                print(f"{ColoresUR.AMARILLO_HITL}🛠️ SUGERENCIA TÉCNICA: {diagnostico['technical_fix']}{ColoresUR.RESET}")

                if reintentos > self.max_reintentos:
                    TM.error("Se ha alcanzado el límite de reintentos. Abortando auditoría.")
                    raise SymbiomemesisError("Resiliencia agotada.", "ERR-QA-FATAL", etapa_actual)
                
                await asyncio.sleep(2) # Pausa de enfriamiento

        return ciclo_completado

# =============================================================================
# 🚀 TEST DE RESILIENCIA STANDALONE
# =============================================================================
if __name__ == "__main__":
    async def run_test():
        cinta_maestra = MallaCognitivaCompartida()
        cinta_maestra.inicializar_auditoria_financiera()
        
        qa = AgenteResilienciaV7()
        try:
            exito = await qa.ejecutar_test_de_resiliencia_completo(
                cinta_maestra, 
                programa_test="DOCTORADO EN INGENIERÍA, CIENCIA Y TECNOLOGÍA"
            )
            if exito:
                print("\n⭐ [SISTEMA] El enjambre ha pasado todas las pruebas de resiliencia.")
        except SymbiomemesisError as se:
            print(f"\n❌ [SISTEMA] El test falló en la etapa {se.etapa}. Código: {se.codigo}")

    asyncio.run(run_test())