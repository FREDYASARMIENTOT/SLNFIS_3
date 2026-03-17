"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.1 - UNIVERSIDAD DEL ROSARIO
MODULO: Test Unitario - Agente Génesis (Fase 1)
UBICACIÓN: /TEST/
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Valida la capacidad del Agente Génesis para recibir parámetros de 
    Facultad, Programa y Asignatura, y generar el arsenal síncrono.
=============================================================================
"""

import os
import sys

# --- AJUSTE DE RUTAS PARA EJECUCIÓN DESDE /TEST ---
# Agregamos la raíz del proyecto al path para importar los módulos de FIS_VERSION8
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
    print("Asegúrese de ejecutar el test desde la raíz del proyecto o verificar la estructura /FIS_VERSION8")
    sys.exit(1)

def ejecutar_test_genesis(facultad: str, programa: str, asignatura: str):
    """
    Inyecta parámetros de entrada y valida la salida física de archivos.
    """
    TM.encabezado("PRUEBA UNITARIA: AGENTE GÉNESIS V8.1")
    
    # 1. Inicialización de la Cinta para el Test
    cinta = MallaCognitivaCompartidaV8()
    cinta.identificador_proyecto = f"TEST_GEN_01_{facultad[:3]}"
    
    # 2. Configuración de Tarea con Parámetros Explícitos
    # Se construye un prompt que el Agente Génesis (Gemini) debe interpretar
    tarea = (f"Generar arsenal forense para la Facultad: {facultad}, "
             f"Programa: {programa}, Asignatura: {asignatura}")
    
    print(f"{ColoresUR_v8.CIAN_FIN}📥 ENTRADA DE PRUEBA:{ColoresUR_v8.RESET}")
    print(f"   • Facultad: {facultad}")
    print(f"   • Programa: {programa}")
    print(f"   • Asignatura: {asignatura}\n")

    try:
        # 3. Invocación del Agente
        agente = FabricaAgentesV8.crear_agente_genesis()
        # Pasamos los parámetros adicionales en kwargs para que el script .py los use
        resultado = agente.ejecutar(
            cinta, 
            tarea, 
            facultad_test=facultad, 
            programa_test=programa, 
            asignatura_test=asignatura
        )
        
        # 4. VALIDACIÓN FÍSICA DE ARTEFACTOS
        TM.evento("VALIDADOR", "Verificando persistencia en ORIGENDATOS...")
        
        # Buscamos si existen los CSVs generados recientemente
        ruta_origen = os.path.join(ruta_raiz, "ORIGENDATOS")
        archivos_creados = [f for f in os.listdir(ruta_origen) if "v8" in f]
        
        if len(archivos_creados) >= 5:
            print(f"\n{ColoresUR_v8.VERDE_AG}✅ TEST EXITOSO:{ColoresUR_v8.RESET}")
            print(f"   • Artefactos detectados: {len(archivos_creados)} archivos.")
            print(f"   • Registro en Cinta: {cinta.bitacora_forense[-1].status}")
            print(f"   • Mensaje Agente: {resultado}")
        else:
            print(f"\n{ColoresUR_v8.VINO}❌ TEST FALLIDO:{ColoresUR_v8.RESET}")
            print(f"   • Se esperaban 5+ archivos, se encontraron: {len(archivos_creados)}")

    except Exception as e:
        TM.error(f"Falla crítica en test_agente_genesis: {e}")

if __name__ == "__main__":
    # PARÁMETROS DE PRUEBA (Modificables para diferentes escenarios)
    TEST_FACULTAD = "ESCUELA DE INGENIERÍA, CIENCIA Y TECNOLOGÍA"
    TEST_PROGRAMA = "DOCTORADO EN INGENIERÍA, CIENCIA Y TECNOLOGÍA"
    TEST_ASIGNATURA = "INTELIGENCIA ARTIFICIAL APLICADA"

    ejecutar_test_genesis(TEST_FACULTAD, TEST_PROGRAMA, TEST_ASIGNATURA)