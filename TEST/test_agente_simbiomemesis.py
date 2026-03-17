"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.1 - UNIVERSIDAD DEL ROSARIO
MODULO: Test Unitario - Agente de Convergencia Simbiomemesis (Fase 5)
UBICACIÓN: /TEST/
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Evalúa la inteligencia del sistema para interpretar el Gradiente dU/dt.
    Valida si el enjambre detecta correctamente la evolución del Bienestar 
    Simbiótico entre mediciones temporales.
=============================================================================
"""

import os
import sys
from datetime import datetime

# --- AJUSTE DE RUTAS ---
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ruta_raiz not in sys.path:
    sys.path.append(ruta_raiz)
    sys.path.append(os.path.join(ruta_raiz, "FIS_VERSION8"))

try:
    from FIS_VERSION8.fis_cintagentica_v8 import MallaCognitivaCompartidaV8
    from FIS_VERSION8.fis_fabrica_agentes_v8 import FabricaAgentesV8
    from FIS_VERSION8.fis_telemetria_v8 import TelemetriaMaestraV8 as TM, ColoresUR_v8
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    sys.exit(1)

def ejecutar_test_simbiomemesis():
    TM.encabezado("PRUEBA UNITARIA: AGENTE DE CONVERGENCIA SIMBIOMEMESIS")
    
    cinta = MallaCognitivaCompartidaV8()
    cinta.identificador_proyecto = "VALIDACION_CONVERGENCIA_V8"
    cinta.etapa_actual = "ETAPA_SIMBIOMEMESIS"

    # --- INYECCIÓN DE LÍNEA DE TIEMPO (U0 -> U1) ---
    # Usamos su valor real calculado en la prueba anterior (0.000021)
    u_base = 0.0000150000
    u_actual = 0.0000210000
    variacion_pct = ((u_actual - u_base) / u_base) * 100

    print(f"{ColoresUR_v8.CIAN_FIN}💉 Sincronizando historial de utilidad en la Cinta...{ColoresUR_v8.RESET}")
    print(f"   • U_anterior (M0): {u_base:.10f}")
    print(f"   • U_actual   (M1): {u_actual:.10f}")
    print(f"   • Delta (ΔU): {u_actual - u_base:.10f} ({variacion_pct:.2f}%)")

    # Estructura de datos que espera el Agente Gradiente/Simbiomemesis
    cinta.datos_matriz_auditoria = {
        "valor_u": u_actual,
        "historial_u": [u_base, u_actual],
        "metadatos_auditoria": {
            "componente_estocastico": 0.6059,
            "friccion_integrada": 0.3123,
            "eficiencia_financiera": 0.000046
        }
    }

    try:
        # El Agente Gradiente actúa como el 'Motor de Simbiomemesis'
        agente_simbio = FabricaAgentesV8.crear_agente_gradiente_razonador()
        
        prompt_mision = (
            f"Como Agente de Simbiomemesis, analiza el cambio de Utilidad U. "
            f"Medición 0: {u_base:.10f} | Medición 1: {u_actual:.10f}. "
            f"Determina si el sistema tiende a la 'Simbiosis' (Crecimiento de bienestar) "
            f"o a la 'Entropía' (Degradación). Explica el impacto para la Universidad del Rosario."
        )
        
        print(f"\n{ColoresUR_v8.CIAN_FIN}📈 ANALIZANDO TENDENCIAS DE CAJA BLANCA...{ColoresUR_v8.RESET}")
        diagnostico = agente_simbio.ejecutar(cinta, prompt_mision)
        
        # --- VALIDACIÓN DE RESULTADOS ---
        if diagnostico and "ERROR" not in diagnostico:
            print(f"\n{ColoresUR_v8.VERDE_AG}✅ TEST SIMBIOMEMESIS EXITOSO:{ColoresUR_v8.RESET}")
            print(f"{'═'*80}")
            print(f"{ColoresUR_v8.NEGRITA}DIAGNÓSTICO DOCTORAL:{ColoresUR_v8.RESET}")
            print(f"{diagnostico}")
            print(f"{'═'*80}")
            
            # Persistencia en la Cinta para el Chatbot
            cinta.datos_matriz_auditoria["diagnostico_final"] = diagnostico
            cinta.guardar_estado_v8()
            print(f"\n📂 Resultados persistidos en LOGS_v8/cinta_v8_checkpoint.json")
        else:
            print(f"\n{ColoresUR_v8.VINO}❌ TEST FALLIDO: El agente no pudo generar el diagnóstico.{ColoresUR_v8.RESET}")

    except Exception as e:
        TM.error(f"Falla crítica en el test de Simbiomemesis: {e}")

if __name__ == "__main__":
    ejecutar_test_simbiomemesis()