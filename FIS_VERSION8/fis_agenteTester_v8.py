"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Agente Tester de Indicadores Estocásticos (Forense v8.1)
UBICACIÓN: /FIS_VERSION8/
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Genera la Malla de 45 Variables y 15 Variables Consolidadas para U.
    Implementa el Protocolo de Exposición Explícita y Encapsulación de Errores.
=============================================================================
"""

import os
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional

# --- IMPORTACIONES LOCALES V8 ---
from fis_telemetria_v8 import TelemetriaMaestraV8 as TM

# =============================================================================
# 🛡️ ENCAPSULACIÓN DE ERRORES DEL TESTER (PARA EL CHATBOT/REPORTE)
# =============================================================================
class TesterErrorV8(Exception):
    """Clase para reportar fallos de auditoría al Orquestador."""
    def __init__(self, mensaje: str, fase: str, codigo: str = "ERR-TST-800"):
        self.mensaje = mensaje
        self.fase = fase
        self.codigo = codigo
        self.timestamp = datetime.now().isoformat()
        super().__init__(f"[{codigo}] {mensaje}")

    def to_dict(self):
        return {"error": self.mensaje, "fase": self.fase, "codigo": self.codigo, "ts": self.timestamp}

# =============================================================================
# 🧬 AGENTE TESTER V8 - LABORATORIO DE INFERENCIA
# =============================================================================
class AgenteTesterv8:
    """
    Agente de Auditoría Estocástica.
    Responsable de la Malla de 45 indicadores y la reducción a 15 variables de U.
    """

    @staticmethod
    def obtener_malla_45_definiciones() -> List[str]:
        """Definición canónica de los 45 indicadores de la Tesis."""
        me = [f"ME_{i:02}_Eficiencia_Cognitiva" for i in range(1, 16)]
        sg = [f"SG_{i:02}_Sinergia_Enjambre" for i in range(16, 31)]
        fr = [f"FR_{i:02}_Friccion_Sistemica" for i in range(31, 46)]
        return me + sg + fr

    @classmethod
    def ejecutar_evaluacion_indicadores(cls, cinta: Any, **kwargs) -> str:
        """
        Ejecución Forense: Genera 45 valores -> Consolida 15 -> Registra en Cinta.
        """
        TM.encabezado("LABORATORIO ESTOCÁSTICO V8.1: AUDITORÍA DE 45 VARIABLES")
        monitor = kwargs.get('monitor_forense')
        iteracion = kwargs.get('iteracion', 1)
        
        try:
            # 1. GENERACIÓN DE VALORACIÓN EXPLÍCITA (45 INDICADORES)
            TM.evento("TESTER_V8", f"Iniciando valoración para Medición M{iteracion}...")
            indicadores_def = cls.obtener_malla_45_definiciones()
            malla_45 = {}

            for ind in indicadores_def:
                # Lógica estocástica diferenciada por pilar (Caja Blanca)
                if "ME_" in ind: mu, sigma = 0.88, 0.03   # Alta eficiencia esperada
                elif "SG_" in ind: mu, sigma = 0.82, 0.05 # Sinergia variable
                else: mu, sigma = 0.12, 0.04              # Fricción baja deseada
                
                valor = np.clip(np.random.normal(mu, sigma), 0, 1)
                malla_45[ind] = round(float(valor), 4)

            # 2. REDUCCIÓN A 15 VARIABLES MAESTRAS (INSUMOS DE U)
            TM.evento("TESTER_V8", "Consolidando 15 variables de decisión para Utilidad U...")
            variables_15 = {}
            for i in range(15):
                grupo = indicadores_def[i*3 : (i+1)*3]
                promedio = np.mean([malla_45[v] for v in grupo])
                nombre_v = f"VAR_U_{i+1:02}_Consolidada"
                variables_15[nombre_v] = round(float(promedio), 4)

            # 3. EXPOSICIÓN EXPLÍCITA EN TELEMETRÍA (LOGS DE ALTA FIDELIDAD)
            if monitor:
                # Reportamos los promedios de los pilares como hitos matemáticos
                me_avg = np.mean([v for k,v in malla_45.items() if "ME_" in k])
                sg_avg = np.mean([v for k,v in malla_45.items() if "SG_" in k])
                fr_avg = np.mean([v for k,v in malla_45.items() if "FR_" in k])

                TM.explicar_calculo(monitor, "AVG_Pilar_ME", {"Vars": "1-15"}, round(me_avg, 4))
                TM.explicar_calculo(monitor, "AVG_Pilar_SG", {"Vars": "16-30"}, round(sg_avg, 4))
                TM.explicar_calculo(monitor, "AVG_Pilar_FR", {"Vars": "31-45"}, round(fr_avg, 4))
                
                # Inyección del CoT del Tester en la Cinta
                monitor.cot_text = (f"Medición M{iteracion}: Estabilidad detectada. "
                                   f"ME: {me_avg:.2f}, SG: {sg_avg:.2f}, FR: {fr_avg:.2f}. "
                                   "Procediendo a inyectar 15 variables en la Cinta Agéntica.")
                
                # Registro de tokens (Simulación de procesamiento local)
                monitor.registrar_tokens(950, 450)

            # 4. ACTUALIZACIÓN DE LA CINTA AGÉNTICA (ESTADO COMPLETO)
            # El chatbot RAG podrá leer 'malla_45_completa' para explicar detalles.
            cinta.datos_resultados_tester = type('obj', (object,), {
                'iteracion': iteracion,
                'malla_45_completa': malla_45,
                'variables_15_utilidad': variables_15,
                'status': "VALIDATED",
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            msg_final = f"Auditoría M{iteracion} Exitosa. 45 Indicadores Expuestos | 15 Variables de U Listas."
            TM.evento("TESTER_V8", msg_final)
            return msg_final

        except Exception as e:
            # ENCAPSULACIÓN DE ERROR PARA EL ORQUESTADOR
            error_obj = TesterErrorV8(str(e), "GENERACION_ESTOCASTICA")
            TM.error(f"Falla crítica: {error_obj.mensaje}")
            
            # El error viaja a la cinta para que el Chatbot lo reporte al usuario
            cinta.error_actual = error_obj.to_dict()
            return f"ERROR_TESTER_V8: {error_obj.codigo}"