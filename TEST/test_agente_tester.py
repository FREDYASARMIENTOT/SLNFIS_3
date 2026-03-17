"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.1 - UNIVERSIDAD DEL ROSARIO
MODULO: Test Unitario - Agente Tester (Fase 3)
UBICACIÓN: /TEST/
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Valida la capacidad del Agente Tester para:
    1. Leer el consolidado de 25,750 clases en /data.
    2. Ejecutar la lógica de auditoría para calcular los 45 indicadores.
    3. Extraer las 15 variables fundamentales para la ecuación de Utilidad U.
=============================================================================
"""

import os
import sys
import pandas as pd

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

def ejecutar_test_tester():
    """
    Prueba la capacidad de análisis estocástico y reducción de datos.
    """
    TM.encabezado("PRUEBA UNITARIA: AGENTE TESTER DE INDICADORES V8.1")
    
    # 1. Inicialización de la Cinta
    cinta = MallaCognitivaCompartidaV8()
    cinta.identificador_proyecto = "TEST_TESTER_45_INDICADORES"
    
    # 2. Localización del insumo (Excel generado por el test ABC)
    ruta_data = os.path.join(ruta_raiz, "data")
    excels = [f for f in os.listdir(ruta_data) if "CONSOLIDADO_ABC_v8" in f and f.endswith(".xlsx")]
    
    if not excels:
        print(f"{ColoresUR_v8.VINO}❌ ERROR: No se encontró insumo en /data. Ejecute test_agente_abc.py primero.{ColoresUR_v8.RESET}")
        return

    archivo_insumo = max([os.path.join(ruta_data, f) for f in excels], key=os.path.getmtime)
    print(f"📂 Analizando insumo: {os.path.basename(archivo_insumo)}")

    # 3. Invocación del Agente vía Fábrica
    tarea = "Evaluar la malla de 45 indicadores institucionales y extraer variables de utilidad."
    
    print(f"{ColoresUR_v8.CIAN_FIN}🧪 EJECUTANDO AUDITORÍA ESTOCÁSTICA...{ColoresUR_v8.RESET}")
    
    try:
        agente = FabricaAgentesV8.crear_agente_tester()
        # El agente Tester procesa el archivo y actualiza los objetos de la cinta
        resultado = agente.ejecutar(cinta, tarea, ruta_archivo=archivo_insumo)
        
        # 4. VALIDACIÓN DE LA MALLA EN CINTA
        malla = cinta.datos_resultados_tester.malla_45_completa
        vars_15 = cinta.datos_resultados_tester.variables_15_utilidad
        
        if malla and len(malla) >= 45:
            print(f"\n{ColoresUR_v8.VERDE_AG}✅ TEST TESTER EXITOSO:{ColoresUR_v8.RESET}")
            print(f"   • Indicadores calculados: {len(malla)} / 45")
            print(f"   • Variables para U extraídas: {len(vars_15)} / 15")
            
            # Muestra de validación forense
            print(f"\n{ColoresUR_v8.CIAN_FIN}📊 MUESTRA DE INDICADORES (CAJA BLANCA):{ColoresUR_v8.RESET}")
            for k, v in list(malla.items())[:5]: # Mostramos los primeros 5
                print(f"     🔹 {k}: {v}")
                
            print(f"\n   • Registro en Cinta: {cinta.bitacora_forense[-1].status}")
            print(f"   • Mensaje Agente: {resultado}")
        else:
            print(f"\n{ColoresUR_v8.VINO}❌ TEST TESTER FALLIDO:{ColoresUR_v8.RESET}")
            print(f"   • Malla incompleta. Detectados: {len(malla) if malla else 0} indicadores.")

    except Exception as e:
        TM.error(f"Falla crítica en test_agente_tester: {e}")

if __name__ == "__main__":
    ejecutar_test_tester()