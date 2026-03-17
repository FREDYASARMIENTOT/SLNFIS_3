"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Human-In-The-Loop (HITL) - Gobernanza y Discrecionalidad (v8.0)
UBICACIÓN: /FIS_VERSION8/
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Punto de control de auditoría científica. Permite al usuario:
    1. MEDIR: Re-iterar la malla de 45 indicadores para generar histórico.
    2. SEGUIR: Aprobar el estado actual y proceder al cálculo de U.
    3. Persistencia estigmérgica de cada punto de decisión.
=============================================================================
"""

import time
import os
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from datetime import datetime

# --- IMPORTACIONES LOCALES V8 ---
from fis_telemetria_v8 import TelemetriaMaestraV8 as TM

# =============================================================================
# 🛡️ ENCAPSULACIÓN DE ERRORES DE GOBERNANZA
# =============================================================================
class HitlErrorV8(Exception):
    """Errores en la fase de intervención humana."""
    def __init__(self, mensaje: str, codigo: str = "ERR-HITL-800"):
        self.mensaje = mensaje
        self.codigo = codigo
        self.timestamp = datetime.now().isoformat()
        super().__init__(f"[{codigo}] {mensaje}")

    def to_dict(self):
        return {"error": self.mensaje, "codigo": self.codigo, "ts": self.timestamp}

# =============================================================================
# 🧬 GESTOR DE INTERVENCIÓN HUMANA V8
# =============================================================================
class GestorDeIntervencionHumanaV8:
    """
    Garante de la Auditoría 360. 
    Permite la toma de decisiones discrecionales sobre la Malla Cognitiva.
    """

    @staticmethod
    def presentar_auditoria_v8(cinta: Any, **kwargs) -> bool:
        """
        Interfaz de decisión para el Orquestador.
        Retorna True para SEGUIR (Avanzar a U), False para MEDIR (Re-iterar).
        """
        TM.encabezado("ESTACIÓN DE MANDO HITL - GOBERNANZA v8.0")
        
        # 1. VALIDACIÓN DE ESTADO DE LA CINTA
        if not hasattr(cinta, 'datos_resultados_tester') or not cinta.datos_resultados_tester:
            error = HitlErrorV8("No hay datos de medición para auditar.", "ERR-HITL-404")
            TM.error(error.mensaje)
            cinta.error_actual = error.to_dict()
            return False

        # 2. RASTREO DE TAPEAGENTS (CONTEXTO PARA EL AUDITOR)
        monitor = kwargs.get('monitor_forense')
        datos = cinta.datos_resultados_tester
        iteracion = getattr(datos, 'iteracion', 0)
        
        # 3. EXPOSICIÓN DE MÉTRICAS CLAVE PARA EL AUDITOR
        TM.evento("HITL_V8", f"Auditoría de Medición M{iteracion} en proceso...")
        
        # Calculamos promedios rápidos para la vista de terminal
        malla = datos.malla_45_completa
        me_avg = np.mean([v for k,v in malla.items() if "ME_" in k])
        sg_avg = np.mean([v for k,v in malla.items() if "SG_" in k])
        fr_avg = np.mean([v for k,v in malla.items() if "FR_" in k])

        # 4. TRAZABILIDAD MATEMÁTICA EN BITÁCORA (Para Streamlit/Chatbot)
        if monitor:
            TM.explicar_calculo(monitor, "Resumen_Malla_M" + str(iteracion), 
                               {"ME": f"{me_avg:.2f}", "SG": f"{sg_avg:.2f}", "FR": f"{fr_avg:.2f}"}, 
                               "ESPERANDO_APROBACION")
            monitor.cot_text = (f"El Auditor Humano está evaluando la Medición M{iteracion}. "
                               f"Se requiere discrecionalidad para persistir el punto o avanzar.")

        # 5. LÓGICA DE DECISIÓN (Simulada para Terminal / Interactiva para Streamlit)
        # En la UI de Streamlit, 'comando' vendrá de un st.button()
        comando = kwargs.get('comando_auditor', None)

        if comando == "MEDIR":
            # PERSISTIR PUNTO PARA FUNCIÓN SIMBIOMEMÉSICA
            TM.evento("HITL_V8", f"Comando MEDIR detectado. Persistiendo rastro de M{iteracion}...")
            cinta.registrar_evento_forense_detallado(
                emisor="AUDITOR_HUMANO",
                receptor="CINTA_V8",
                mensaje=f"Re-medición solicitada para M{iteracion}. Generando histórico de gradiente.",
                entrada=f"ME:{me_avg:.2f}, SG:{sg_avg:.2f}",
                salida="RE-ITERAR_TESTER"
            )
            return False # Instrucción al orquestador para repetir AgenteTester

        elif comando == "SEGUIR":
            # BLOQUEAR ESTADO Y AVANZAR A UTILIDAD U
            TM.evento("HITL_V8", "Comando SEGUIR detectado. Bloqueando Malla para resolución de U.")
            cinta.registrar_evento_forense_detallado(
                emisor="AUDITOR_HUMANO",
                receptor="CINTA_V8",
                mensaje=f"Aprobación de M{iteracion} concedida. Procediendo a Fase Matemática.",
                entrada="Comando_SEGUIR",
                salida="PROXIMO:AGENTE_MATH_U"
            )
            return True # Instrucción para avanzar al Agente de Utilidad U

        # Si no hay comando (espera interactiva), lanzamos aviso
        return False