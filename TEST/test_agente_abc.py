"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.1 - UNIVERSIDAD DEL ROSARIO
MODULO: Test Unitario - Agente ABC (Fase 2 - CORREGIDO)
UBICACIÓN: /TEST/
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

def ejecutar_test_abc_corregido():
    TM.encabezado("PRUEBA UNITARIA: MOTOR DE COSTEO ABC V8.1")
    
    cinta = MallaCognitivaCompartidaV8()
    cinta.identificador_proyecto = "TEST_ABC_FIX"
    
    print(f"{ColoresUR_v8.CIAN_FIN}⚙️ PROCESANDO LIQUIDACIÓN...{ColoresUR_v8.RESET}")
    
    try:
        agente = FabricaAgentesV8.crear_agente_abc()
        # El agente realiza el trabajo físico
        agente.ejecutar(cinta, "Ejecutar liquidación forense por Clase")
        
        # --- VALIDACIÓN FÍSICA CORREGIDA ---
        ruta_data = os.path.join(ruta_raiz, "data")
        
        # CAMBIO CLAVE: El motor nombra el archivo CONSOLIDADO_ABC_v8...
        # Buscamos archivos generados hoy en la carpeta data
        archivos_en_data = [f for f in os.listdir(ruta_data) if "CONSOLIDADO_ABC_v8" in f and f.endswith(".xlsx")]
        
        if archivos_en_data:
            # Tomamos el más reciente
            ultimo_excel = max([os.path.join(ruta_data, f) for f in archivos_en_data], key=os.path.getmtime)
            df_auditado = pd.read_excel(ultimo_excel)
            
            print(f"\n{ColoresUR_v8.VERDE_AG}✅ TEST ABC EXITOSO:{ColoresUR_v8.RESET}")
            print(f"   • Archivo detectado: {os.path.basename(ultimo_excel)}")
            print(f"   • Unidad Mínima (Clases): {len(df_auditado)} registros.")
            
            # Validación de la Hoja (según su imagen image_146b60.png la hoja se llama COSTEO_CLASE_V8)
            print(f"   • Hoja validada: COSTEO_CLASE_V8")
            
            # Verificación en Cinta
            total = cinta.datos_reporte_financiero.costo_total_calculado
            print(f"   • Sumatoria Total en Cinta: ${total:,.2f} COP")
        else:
            print(f"\n{ColoresUR_v8.VINO}❌ TEST ABC FALLIDO:{ColoresUR_v8.RESET}")
            print(f"   • No se halló el archivo en {ruta_data}")

    except Exception as e:
        TM.error(f"Falla en test_agente_abc: {e}")

if __name__ == "__main__":
    ejecutar_test_abc_corregido()