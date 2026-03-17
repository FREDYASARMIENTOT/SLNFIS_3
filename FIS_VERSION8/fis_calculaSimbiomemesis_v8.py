"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Analista de Gradiente y Razón de Cambio (Forense v8.1)
UBICACIÓN: /FIS_VERSION8/
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Motor de análisis de trayectoria. Calcula dU/dM y vectores de cambio.
    Implementa:
    1. Trazabilidad de Derivadas Discretas.
    2. Diagnóstico de Convergencia (Simbiosis vs Entropía).
    3. Encapsulación de errores para el Orquestador y Chatbot.
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
# 🛡️ ENCAPSULACIÓN DE ERRORES DE ANÁLISIS
# =============================================================================
class GradientErrorV8(Exception):
    """Errores en el cálculo de la razón de cambio."""
    def __init__(self, mensaje: str, fase: str, codigo: str = "ERR-GRAD-800"):
        self.mensaje = mensaje
        self.fase = fase
        self.codigo = codigo
        self.timestamp = datetime.now().isoformat()
        super().__init__(f"[{codigo}] {mensaje}")

    def to_dict(self):
        return {"error": self.mensaje, "fase": self.fase, "codigo": self.codigo, "ts": self.timestamp}

# =============================================================================
# 🧬 MODELO DE RESULTADOS ANALÍTICOS
# =============================================================================
class ResultadoGradienteV8(BaseModel):
    iteracion_actual: int
    utilidad_n: float
    utilidad_n_minus_1: float
    delta_u: float
    razon_de_cambio: float
    analisis_convergencia: str
    diagnostico_forense: str

# =============================================================================
# 📈 MOTOR MATEMÁTICO SYMBIOMEMESIS V8
# =============================================================================
class MotorMatematicoSymbiomemesisV8:
    """
    Inteligencia Analítica para Derivadas Parciales Discretas.
    Determina si el enjambre está optimizando la utilidad en el tiempo.
    """

    @staticmethod
    def analizar_gradiente_cambio(cinta: Any, **kwargs) -> str:
        """
        Calcula dU/dM = (U_n - U_{n-1}) / ΔM.
        Registra el razonamiento matemático en la Cinta y Telemetría.
        """
        TM.encabezado("ANÁLISIS DE GRADIENTE SYMBIOMEMÉSICO - v8.1")
        monitor = kwargs.get('monitor_forense')

        try:
            # 1. RECUPERACIÓN DE MEMORIA HISTÓRICA (Caja Blanca)
            # Buscamos en la cinta el valor de U recién calculado y el histórico
            historial = getattr(cinta, 'datos_matriz_auditoria', None)
            
            if not historial or "valor_u" not in historial:
                raise GradientErrorV8("No se encontró 'valor_u' en la Cinta para comparar.", "RECUPERACION_DATA")

            u_n = historial["valor_u"]
            # Recuperamos U anterior (o simulamos si es la primera iteración M1)
            u_n_1 = historial.get("utilidad_u_previa", u_n * 0.92) 
            iter_n = historial.get("iteracion", 1)

            # 2. CÁLCULO DE LA DERIVADA DISCRETA (dU/dM)
            delta_u = u_n - u_n_1
            # Razón de cambio por unidad de iteración
            razon_cambio = delta_u / 1.0 

            # 3. DIAGNÓSTICO DE CONVERGENCIA SISTÉMICA
            if razon_cambio > 0.05:
                estado = "CRECIMIENTO_SIMBIÓTICO"
                diag = "Las variables estocásticas están superando la fricción administrativa."
            elif razon_cambio < -0.05:
                estado = "ENTROPÍA_ADMINISTRATIVA"
                diag = "La fricción institucional está degradando la utilidad del sistema."
            else:
                estado = "ESTABILIDAD_SISTÉMICA"
                diag = "El sistema ha alcanzado un punto de equilibrio en el costeo ABC."

            # 4. ESTRUCTURACIÓN FORENSE
            res = ResultadoGradienteV8(
                iteracion_actual=iter_n,
                utilidad_n=round(u_n, 6),
                utilidad_n_minus_1=round(u_n_1, 6),
                delta_u=round(delta_u, 6),
                razon_de_cambio=round(razon_cambio, 6),
                analisis_convergencia=estado,
                diagnostico_forense=diag
            )

            # 5. REGISTRO EN TELEMETRÍA (Desglose Paso a Paso)
            if monitor:
                TM.explicar_calculo(
                    monitor, 
                    "Derivada_Discreta_dU/dM", 
                    {"U_actual": res.utilidad_n, "U_previa": res.utilidad_n_minus_1}, 
                    res.razon_de_cambio
                )
                monitor.pasos_matematicos.append(f"Diagnóstico: {res.analisis_convergencia}")
                monitor.pasos_matematicos.append(f"Interpretación: {res.diagnostico_forense}")
                monitor.registrar_tokens(800, 300)

            # 6. ACTUALIZACIÓN DE LA CINTA V8
            # Guardamos el gradiente y preparamos el u_n para la siguiente iteración
            cinta.datos_matriz_auditoria["gradiente_v8"] = res.model_dump()
            cinta.datos_matriz_auditoria["utilidad_u_previa"] = u_n 

            # 7. NOTIFICACIÓN AL ORQUESTADOR
            msg_final = (f"Gradiente M{res.iteracion_actual}: ΔU={res.delta_u:+.4f}. "
                         f"Estado: {res.analisis_convergencia}. {res.diagnostico_forense}")
            
            TM.evento("AGENTE_GRADIENTE", msg_final)
            return msg_final

        except GradientErrorV8 as ge:
            TM.error(f"Error en Gradiente: {ge.mensaje}")
            cinta.error_actual = ge.to_dict()
            return f"ERROR_GRADIENTE: {ge.codigo}"
        
        except Exception as e:
            err_msg = f"Fallo no controlado en análisis de gradiente: {str(e)}"
            TM.error(err_msg)
            return "ERROR_SISTEMICO_GRADIENTE"