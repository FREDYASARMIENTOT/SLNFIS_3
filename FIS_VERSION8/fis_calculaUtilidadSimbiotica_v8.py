"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Motor de Cálculo de Utilidad Simbiótica Escalar (Forense v8.1)
UBICACIÓN: /FIS_VERSION8/
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Calcula el escalar U con trazabilidad total.
    Implementa:
    1. Encapsulación de errores matemáticos.
    2. Desglose de Caja Blanca para el Chatbot RAG.
    3. Integración con Telemetría de alta fidelidad.
=============================================================================
"""

import os
import numpy as np
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

# --- IMPORTACIONES LOCALES V8 ---
from fis_telemetria_v8 import TelemetriaMaestraV8 as TM

# =============================================================================
# 🛡️ ENCAPSULACIÓN DE ERRORES MATEMÁTICOS
# =============================================================================
class MathErrorU_V8(Exception):
    """Errores específicos del cálculo de Utilidad U."""
    def __init__(self, mensaje: str, componente: str, codigo: str = "ERR-MATH-U8"):
        self.mensaje = mensaje
        self.componente = componente
        self.codigo = codigo
        self.timestamp = datetime.now().isoformat()
        super().__init__(f"[{codigo}] {mensaje}")

    def to_dict(self):
        return {
            "error": self.mensaje, 
            "componente_fallido": self.componente, 
            "codigo": self.codigo, 
            "ts": self.timestamp
        }

# =============================================================================
# 🧬 MODELO DE RESULTADOS (CAJA BLANCA)
# =============================================================================
class ResultadoUtilidadU(BaseModel):
    valor_u: float
    componente_financiero: float
    componente_estocastico: float
    friccion_detectada: float
    iteracion: int
    formula_aplicada: str = "U = (Σ_Estocastico / (1 + F)) * Eficiencia_Fin"
    pasos_detalle: List[str]

# =============================================================================
# 📐 MOTOR DE CÁLCULO SYMBIOMEMESIS
# =============================================================================
class AgenteUtilidadSimbioticaV8:
    """
    Calculador Determinista de Utilidad U.
    Inyecta transparencia algorítmica en la Cinta Agéntica.
    """

    @staticmethod
    def calcular_utilidad_u_puntual(cinta: Any, **kwargs) -> str:
        """
        Método de resolución escalar. 
        Recupera 15 variables del Tester y Reporte ABC.
        """
        TM.encabezado("CÁLCULO DE UTILIDAD SIMBIÓTICA U - v8.1")
        monitor = kwargs.get('monitor_forense')

        try:
            # 1. VALIDACIÓN DE INSUMOS (ORQUESTADOR / CINTA)
            if not hasattr(cinta, 'datos_resultados_tester'):
                raise MathErrorU_V8("Faltan 15 variables estocásticas del Tester", "ESTOCASTICO")
            
            if not hasattr(cinta, 'datos_reporte_financiero'):
                raise MathErrorU_V8("Falta reporte de costos ABC", "FINANCIERO")

            # 2. PROCESAMIENTO COMPONENTE ESTOCÁSTICO (Las 15 variables consolidadas)
            # Extraemos los valores de las 15 variables de la Cinta v8
            vars_15 = cinta.datos_resultados_tester.variables_15_utilidad
            val_estocastico = np.mean(list(vars_15.values()))

            # 3. PROCESAMIENTO COMPONENTE FINANCIERO (Eficiencia)
            costo_total = cinta.datos_reporte_financiero.costo_total_calculado
            if costo_total <= 0:
                raise MathErrorU_V8("Costo total nulo o negativo impide normalización", "FINANCIERO")
            
            # Base UR de normalización: 1 millón de pesos por unidad de utilidad base
            eficiencia_fin = 1000000 / costo_total

            # 4. DETERMINACIÓN DE FRICCIÓN (F)
            # Calculada dinámicamente: (Costos_Indirectos / Costos_Directos) * Factor_Sistemico
            desglose_abc = cinta.datos_reporte_financiero.desglose_de_costos_por_categoria
            ind = desglose_abc.get('Costo_Indirecto_Total', 1)
            dir_ = desglose_abc.get('Costo_Directo_Total', 1)
            
            friccion_base = (ind / dir_) * 0.5 # Ponderación v8
            friccion_sistemica = np.mean([v for k,v in cinta.datos_resultados_tester.malla_45_completa.items() if "FR_" in k])
            
            friccion_final = round((friccion_base + friccion_sistemica) / 2, 4)

            # 5. ECUACIÓN MAESTRA SYMBIOMEMESIS
            utilidad_u = (val_estocastico / (1 + friccion_final)) * eficiencia_fin

            # 6. CONSTRUCCIÓN DE CAJA BLANCA PARA EL CHATBOT
            pasos = [
                f"Σ 15 Vars Estocásticas (μ): {val_estocastico:.4f}",
                f"Factor de Eficiencia Financiera: {eficiencia_fin:.4f} (Base 1M/Costo)",
                f"Fricción Integrada (Adm+Sist): {friccion_final:.4f}",
                f"Resolución: ({val_estocastico:.4f} / {1 + friccion_final:.4f}) * {eficiencia_fin:.4f}"
            ]

            res = ResultadoUtilidadU(
                valor_u=round(utilidad_u, 6),
                componente_financiero=round(eficiencia_fin, 6),
                componente_estocastico=round(val_estocastico, 6),
                friccion_detectada=friccion_final,
                iteracion=cinta.datos_resultados_tester.iteracion,
                pasos_detalle=pasos
            )

            # 7. REGISTRO EN TELEMETRÍA Y CINTA
            if monitor:
                TM.explicar_calculo(monitor, "Ecuación_Maestra_U", {"M": res.iteracion}, res.valor_u)
                for p in pasos:
                    monitor.pasos_matematicos.append(p)
                monitor.registrar_tokens(1100, 350)

            # Persistencia en la Matriz de Auditoría de la Cinta
            cinta.datos_matriz_auditoria = {
                "valor_u": res.valor_u,
                "timestamp": datetime.now().isoformat(),
                "auditoria_forense": res.model_dump()
            }

            msg_final = f"U = {res.valor_u} calculada para Iteración {res.iteracion}. Caja Blanca disponible."
            TM.evento("AGENTE_MATH_U", msg_final)
            return msg_final

        except MathErrorU_V8 as me:
            TM.error(f"Falla en Componente: {me.componente} | {me.mensaje}")
            cinta.error_actual = me.to_dict()
            return f"ERROR_MATH_U: {me.codigo}"
        
        except Exception as e:
            msg = f"Error no controlado en cálculo U: {str(e)}"
            TM.error(msg)
            return "ERROR_DESCONOCIDO_MATH"