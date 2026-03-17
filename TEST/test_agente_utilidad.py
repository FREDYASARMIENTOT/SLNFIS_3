"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.1 - UNIVERSIDAD DEL ROSARIO
MODULO: Test Unitario - Agente Utilidad U (Fase 4 - RECTIFICACIÓN PREFIJOS)
=============================================================================
"""
import os
import sys

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ruta_raiz not in sys.path:
    sys.path.append(ruta_raiz)
    sys.path.append(os.path.join(ruta_raiz, "FIS_VERSION8"))

try:
    from FIS_VERSION8.fis_cintagentica_v8 import MallaCognitivaCompartidaV8, ReporteFinancieroV8
    from FIS_VERSION8.fis_fabrica_agentes_v8 import FabricaAgentesV8
    from FIS_VERSION8.fis_telemetria_v8 import TelemetriaMaestraV8 as TM, ColoresUR_v8
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    sys.exit(1)

def ejecutar_test_utilidad_u_final():
    TM.encabezado("PRUEBA UNITARIA: CÁLCULO DE UTILIDAD SIMBIÓTICA U")
    
    cinta = MallaCognitivaCompartidaV8()
    
    print(f"{ColoresUR_v8.CIAN_FIN}💉 Inyectando ADN Matemático con Prefijos Estrictos (ME_, SG_, FR_)...{ColoresUR_v8.RESET}")
    
    # 1. GENERACIÓN DINÁMICA DE LA MALLA PARA EVITAR 'EMPTY SLICE'
    malla_mock = {}
    vars_mock = {}
    
    # Simulamos 15 indicadores por pilar para la malla 45
    for i in range(1, 16):
        malla_mock[f"ME_{i:02d}_Eficiencia_Cognitiva"] = 0.8808
        malla_mock[f"SG_{i:02d}_Sinergia_Grupal"] = 0.8122
        malla_mock[f"FR_{i:02d}_Friccion_Sistema"] = 0.1246

    # Simulamos las 15 variables consolidadas (5 por pilar)
    for i in range(1, 6):
        vars_mock[f"ME_VAR_{i:02d}_Utilidad"] = 0.8808
        vars_mock[f"SG_VAR_{i:02d}_Utilidad"] = 0.8122
        vars_mock[f"FR_VAR_{i:02d}_Utilidad"] = 0.1246

    cinta.datos_resultados_tester.malla_45_completa = malla_mock
    cinta.datos_resultados_tester.variables_15_utilidad = vars_mock
    
    # 2. INYECCIÓN DEL REPORTE FINANCIERO (Denominador de la Ecuación)
    cinta.datos_reporte_financiero = ReporteFinancieroV8(
        costo_total_calculado=21645450000.0,
        desglose_de_costos_por_categoria={"DIRECTO": 15000000000.0, "INDIRECTO": 6645450000.0}
    )

    try:
        agente_u = FabricaAgentesV8.crear_agente_matematico_u()
        tarea = "Resolver la ecuación de Utilidad Escalar U con base en los arreglos estocásticos."
        
        print(f"{ColoresUR_v8.CIAN_FIN}🧮 CALCULANDO ESCALAR U (BIENESTAR SIMBIÓTICO)...{ColoresUR_v8.RESET}")
        agente_u.ejecutar(cinta, tarea)
        
        # Extracción del valor U
        valor_u = cinta.datos_matriz_auditoria.get('valor_u', 0)
        
        if valor_u is not None and str(valor_u) != 'nan' and valor_u > 0:
            print(f"\n{ColoresUR_v8.VERDE_AG}✅ TEST DE UTILIDAD EXITOSO:{ColoresUR_v8.RESET}")
            # Formateamos con notación científica o más decimales para evitar que se vea como 0.0000
            print(f"   • BIENESTAR SIMBIÓTICO (U): {valor_u:.10f}")
            
            # Intentamos extraer el detalle si existe
            if 'auditoria_forense' in cinta.datos_matriz_auditoria:
                audit = cinta.datos_matriz_auditoria['auditoria_forense']
                print(f"   • Factor Estocástico (Σ): {audit.get('componente_estocastico', 0):.4f}")
                print(f"   • Fricción Integrada: {audit.get('friccion_detectada', 0):.4f}")
                print(f"   • Eficiencia Financiera: {audit.get('componente_financiero', 0):.10f}")
        else:
            print(f"\n{ColoresUR_v8.VINO}❌ TEST FALLIDO POR INDETERMINACIÓN:{ColoresUR_v8.RESET}")
            print(f"   • Resultado: {valor_u}")

    except Exception as e:
        TM.error(f"Falla crítica: {e}")

if __name__ == "__main__":
    ejecutar_test_utilidad_u_final()