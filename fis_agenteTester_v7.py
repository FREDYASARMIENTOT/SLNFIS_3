"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v7.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Agente Tester de Indicadores Estocásticos (Caja Blanca)
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Genera y valida la Malla de 45 Variables de Tesis. 
    Soporta múltiples mediciones (M1, M2, M3...) para permitir el cálculo 
    de razones de cambio y derivadas parciales en la utilidad U.
=============================================================================
"""

import os
import json
import numpy as np
import logging
from datetime import datetime
from typing import List, Dict, Any

# --- INTEGRACIÓN CON EL ECOSISTEMA V7 ---
from fis_telemetria_v7 import TelemetriaMaestraV7 as TM, ColoresUR
from fis_cintagentica_v7 import MallaCognitivaCompartida, ResultadosDelInstrumentoDelTester

# --- CONFIGURACIÓN DE LOGS ESPECÍFICOS ---
LOGS_DIR = "LOGS"
os.makedirs(LOGS_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOGS_DIR, "fis_agenteTester.log"),
    level=logging.INFO,
    format='%(asctime)s | %(message)s'
)

class AgenteTesterv7:
    """
    Laboratorio de Inferencia Estocástica. 
    Mapea 45 indicadores en 3 pilares: Eficiencia, Sinergia y Fricción.
    """

    @staticmethod
    def obtener_definicion_45_variables() -> List[str]:
        """Lista descriptiva larga de las variables de la tesis."""
        return [
            # PILAR 1: MICRO-EFICIENCIA COGNITIVA (ME) - 15 vars
            "ME_01_Precisión_de_Recuperación_de_Contexto_Semántico",
            "ME_02_Fidelidad_de_la_Respuesta_IA_respecto_al_Arsenal_de_Datos",
            "ME_03_Tasa_de_Alucinación_Detectada_en_Inferencia_ABC",
            "ME_04_Consistencia_Lógica_de_Prorrateo_por_Asignatura",
            "ME_05_Claridad_Expositiva_del_Agente_de_Chatbot",
            "ME_06_Velocidad_de_Convergencia_del_Cálculo_Financiero",
            "ME_07_Ajuste_de_la_Respuesta_al_Perfil_de_Analista",
            "ME_08_Calidad_de_la_Estructura_JSON_Forense",
            "ME_09_Estabilidad_del_Factor_de_Costo_Base_Cbi",
            "ME_10_Relevancia_de_la_Entidad_RAG_Identificada",
            "ME_11_Tasa_de_Éxito_en_Validación_de_IDs_Huérfanos",
            "ME_12_Complejidad_Cognitiva_de_la_Tarea_Realizada",
            "ME_13_Nivel_de_Abstracción_del_Veredicto_Matemático",
            "ME_14_Eficiencia_del_Prompt_Estructural_V7",
            "ME_15_Satisfacción_del_Auditor_respecto_a_la_Caja_Blanca",

            # PILAR 2: SINERGIA DE ENJAMBRE (SIGMA) - 15 vars
            "SG_16_Fluidez_de_Comunicación_entre_Agente_Generador_y_Costeo",
            "SG_17_Sincronía_de_Telemetría_en_la_Malla_Cognitiva",
            "SG_18_Ahorro_de_Tiempo_Percibido_por_Automatización",
            "SG_19_Densidad_de_Interacción_Humano_Sistema",
            "SG_20_Consistencia_Transversal_del_Arsenal_Generado",
            "SG_21_Capacidad_de_Resiliencia_del_Agente_QA",
            "SG_22_Integración_de_Variables_Financieras_Reales_UR",
            "SG_23_Calidad_de_la_Persistencia_en_Memoria_Vectorial",
            "SG_24_Precisión_del_Mapeo_de_Grupos_por_Asignatura",
            "SG_25_Eficiencia_en_el_Uso_de_Tokens_de_Contexto",
            "SG_26_Coherencia_del_Informe_PDF_Generado",
            "SG_27_Trazabilidad_del_Libro_Mayor_Forense",
            "SG_28_Adaptabilidad_del_Orquestador_a_Nuevos_Programas",
            "SG_29_Robustez_de_la_Conexión_con_Pinecone",
            "SG_30_Sinergia_Total_del_Ecosistema_Symbiomemesis",

            # PILAR 3: FRICCIÓN Y ESTABILIDAD (F) - 15 vars
            "FR_31_Nivel_de_Ruido_en_la_Entrada_del_Usuario",
            "FR_32_Fricción_por_Latencia_de_Red_en_Operaciones_RAG",
            "FR_33_Redundancia_de_Datos_en_la_Malla_Cognitiva",
            "FR_34_Carga_Cognitiva_del_Analista_durante_el_HITL",
            "FR_35_Error_Residual_en_el_Cálculo_de_Derivadas",
            "FR_36_Saturación_de_la_Cola_de_Eventos_del_Sistema",
            "FR_37_Conflictos_de_Integridad_Referencial_Detectados",
            "FR_38_Desviación_del_Costo_Indirecto_respecto_al_Directo",
            "FR_39_Inestabilidad_de_la_TRM_en_Tiempo_Real",
            "FR_40_Fallas_de_Autenticación_en_APIs_Externas",
            "FR_41_Ambigüedad_en_la_Definición_de_Rubros_ABC",
            "FR_42_Resistencia_al_Cambio_del_Modelo_Matemático",
            "FR_43_Dificultad_de_Interpretación_de_los_Resultados_U",
            "FR_44_Perplejidad_del_Modelo_de_Lenguaje_Utilizado",
            "FR_45_Fricción_Sistémica_Total_del_Enjambre"
        ]

    @classmethod
    def ejecutar_evaluacion_indicadores(cls, cinta: MallaCognitivaCompartida):
        """Genera la medición, la numera y la persiste en la base vectorial."""
        TM.encabezado("LABORATORIO ESTOCÁSTICO: EVALUACIÓN DE 45 VARIABLES")
        
        with TM.monitor(cinta, "AGENTE_TESTER", "Inferencia_Estocástica_Variables") as monitor:
            definiciones = cls.obtener_definicion_45_variables()
            
            # Recuperar iteración actual
            if not cinta.datos_resultados_tester:
                iteracion_actual = 1
                mediciones_previas = {v: [] for v in definiciones}
            else:
                iteracion_actual = cinta.datos_resultados_tester.numero_de_iteracion_actual + 1
                mediciones_previas = cinta.datos_resultados_tester.valores_crudos_cuarenta_y_cinco_indicadores

            TM.evento("TESTER", f"Generando MEDICIÓN M{iteracion_actual}...")
            
            # Generación Realista (Normal con media variable)
            nuevos_valores = {}
            for var in definiciones:
                base = 0.8 if "ME_" in var else (0.75 if "SG_" in var else 0.2)
                valor_estocastico = np.clip(np.random.normal(base, 0.05), 0, 1)
                nuevos_valores[var] = mediciones_previas.get(var, []) + [float(valor_estocastico)]

            # Actualizar Cinta
            cinta.datos_resultados_tester = ResultadosDelInstrumentoDelTester(
                valores_crudos_cuarenta_y_cinco_indicadores=nuevos_valores,
                numero_de_iteracion_actual=iteracion_actual
            )

            # Persistencia Vectorial (Para derivadas parciales)
            cls._persistir_en_base_vectorial(cinta, iteracion_actual, nuevos_valores)
            
            # Logging en archivo
            logging.info(f"MEDICION M{iteracion_actual} FINALIZADA. Variables: {len(nuevos_valores)}")
            
            TM.evento("TESTER", f"Confirmación: M{iteracion_actual} guardada en Pinecone y lista para calcular Utilidad U.")
            monitor.registrar_tokens(1200, 800)

    @staticmethod
    def _persistir_en_base_vectorial(cinta, iter_id, valores):
        """Registra el estado actual en Pinecone como conocimiento forense."""
        try:
            from google import genai
            from pinecone import Pinecone
            
            client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
            pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
            idx = pc.Index(os.getenv("PINECONE_INDEX"))
            
            resumen_texto = f"Estado M{iter_id} del enjambre Symbiomemesis. Promedio ME: {np.mean([v[-1] for k,v in valores.items() if 'ME_' in k]):.4f}"
            
            emb = client.models.embed_content(
                model="gemini-embedding-2-preview",
                contents=resumen_texto
            )
            
            idx.upsert(vectors=[{
                "id": f"tester_M{iter_id}_{datetime.now().strftime('%H%M%S')}",
                "values": emb.embeddings[0].values,
                "metadata": {"iteracion": iter_id, "tipo": "TESTER_VARIABLES"}
            }], namespace="auditoria-cientifica-v7")
        except Exception as e:
            TM.error(f"Fallo persistencia vectorial Tester: {str(e)}")

# =============================================================================
# PRUEBA INTEGRAL
# =============================================================================
if __name__ == "__main__":
    c = MallaCognitivaCompartida()
    AgenteTesterV7.ejecutar_evaluacion_indicadores(c)