"""
Script de Prueba Aislada: FASE 1 - Generación de Arsenal de Datos
"""
import os
from fis_cintagentica_v7 import MallaCognitivaCompartida
from fis_generador_csvs_v7 import AgenteGeneradorFisV7

try:
    from infra.console import InterfazTerminal as Consola
except ImportError:
    class Consola:
        @staticmethod
        def encabezado_principal(m): print(f"\n{'='*60}\n{m}\n{'='*60}")
        @staticmethod
        def evento_agente(a, m, **k): print(f"[{a}] {m}")
        @staticmethod
        def sistema(m): print(f"[*] {m}")

def probar_generacion_datos():
    Consola.encabezado_principal("TEST AISLADO: FASE 1 (GENERACIÓN DE DATOS V7)")
    
    # 1. Instanciar la Cinta y conectar a Pinecone
    Consola.sistema("Conectando Malla Cognitiva y Memoria Vectorial...")
    cinta = MallaCognitivaCompartida()
    cinta.inicializar_auditoria_financiera()
    
    # 2. Instanciar y ejecutar el Agente Generador
    Consola.evento_agente("AGENTE_DATOS", "Iniciando forjado del Arsenal de Datos (CSVs)...")
    generador = AgenteGeneradorFisV7(raw_data_path="./data")
    
    try:
        # Ejecuta la creación de los 5 archivos
        generador.ejecutar_plan_total()
        
        # 3. Registrar el éxito en la Cinta (Esto sube el evento a Pinecone)
        cinta.registrar_evento_forense_detallado(
            emisor="AGENTE_DATOS_V7", 
            receptor="MALLA_COGNITIVA",
            mensaje=f"Arsenal de datos (5 CSVs) generado exitosamente con timestamp: {generador.timestamp}"
        )
        cinta.cambiar_etapa_del_enjambre("ETAPA_COSTEO_ABC_V7", "TesterHumano")

        # 4. Validar resultados físicos
        print(f"\n✅ Archivos detectados en la carpeta ORIGENDATOS (Timestamp: {generador.timestamp}):")
        archivos_generados = [f for f in os.listdir("ORIGENDATOS") if generador.timestamp in f]
        for arch in archivos_generados:
            print(f"  📄 {arch}")
            
        # 5. Validar rastro vectorial
        print("\n🧠 Validación de Pinecone (RAG):")
        ultimo_registro = cinta.bitacora_forense_del_enjambre[-1]
        print(f"  Vector ID guardado: {ultimo_registro.vector_id}")
        
    except Exception as e:
        print(f"\n❌ Error durante la generación de datos: {str(e)}")

if __name__ == "__main__":
    probar_generacion_datos()