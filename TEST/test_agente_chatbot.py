"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.1 - UNIVERSIDAD DEL ROSARIO
MODULO: Test Unitario - Agente Chatbot RAG (Fase 6 - FIX ARGUMENTOS)
=============================================================================
"""
import os
import sys
import json

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

def ejecutar_test_chatbot_final():
    TM.encabezado("PRUEBA FINAL: CONSULTOR RAG CON MEMORIA PERSISTENTE")
    
    cinta = MallaCognitivaCompartidaV8()
    
    # --- CARGA DE MEMORIA FÍSICA ---
    print(f"{ColoresUR_v8.CIAN_FIN}📂 Cargando Checkpoint de LOGS_v8...{ColoresUR_v8.RESET}")
    ruta_json = os.path.join(ruta_raiz, "LOGS_v8", "cinta_v8_checkpoint.json")
    
    if os.path.exists(ruta_json):
        try:
            with open(ruta_json, "r", encoding="utf-8") as f:
                data = json.load(f)
                cinta.datos_matriz_auditoria = data.get("datos_matriz_auditoria", {})
                
                diagnostico_crudo = cinta.datos_matriz_auditoria.get('diagnostico_final', 'Sin diagnóstico en memoria')
                diagnostico_seguro = str(diagnostico_crudo) if diagnostico_crudo else "Sin diagnóstico"
                
                print(f"✅ Memoria recuperada: {diagnostico_seguro[:80]}...")
        except Exception as e:
            print(f"⚠️ Error al leer JSON de la Cinta: {e}")
    else:
        print("⚠️ No se encontró checkpoint. Usando memoria volátil.")

    try:
        agente_chat = FabricaAgentesV8.crear_agente_chatbot_rag()
        pregunta = "¿Qué significa el estado de 'Estabilidad Sistémica' detectado y cómo afecta a la Facultad?"
        
        print(f"\n{ColoresUR_v8.AMARILLO_HITL}👤 AUDITOR:{ColoresUR_v8.RESET} {pregunta}")
        print(f"{ColoresUR_v8.CIAN_FIN}🤖 AGENTE RAG PENSANDO...{ColoresUR_v8.RESET}\n")
        
        # FIX CLAVE: Pasamos explícitamente prompt=pregunta para que la herramienta interna lo reciba
        resultado_tupla = agente_chat.ejecutar(cinta, pregunta, prompt=pregunta)
        
        # El chatbot v8 devuelve una tupla: (Respuesta_Texto, Contexto_Vectorial)
        if isinstance(resultado_tupla, tuple):
            respuesta = resultado_tupla[0]
        else:
            respuesta = str(resultado_tupla)
        
        if respuesta and "ERROR_AGENTE_V8" not in respuesta:
            print(f"{ColoresUR_v8.VERDE_AG}✅ RESPUESTA DEL CHATBOT:{ColoresUR_v8.RESET}")
            print(f"{'═'*80}")
            print(f"{respuesta}")
            print(f"{'═'*80}")
        else:
            print(f"\n{ColoresUR_v8.VINO}❌ FALLA EN EL CHATBOT:{ColoresUR_v8.RESET}\n{respuesta}")

    except Exception as e:
        TM.error(f"Falla en el test: {e}")

if __name__ == "__main__":
    ejecutar_test_chatbot_final()