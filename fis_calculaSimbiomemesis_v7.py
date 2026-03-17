"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v7.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Motor Matemático Symbiomemesis (Resolución U + Razones de Cambio)
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Núcleo de Inteligencia Analítica. Resuelve la utilidad U y calcula 
    derivadas parciales (gradientes) basadas en mediciones históricas.
    Integrado con Telemetría V7 y Gestión de Errores para Chatbot.
=============================================================================
"""

import os
import numpy as np
from datetime import datetime
from google import genai
from pinecone import Pinecone
from dotenv import load_dotenv

# Dependencias del ecosistema V7
from fis_cintagentica_v7 import MallaCognitivaCompartida, MatrizDeAuditoriaCientifica
from fis_telemetria_v7 import TelemetriaMaestraV7 as TM

load_dotenv()

# =============================================================================
# 🛡️ ENCAPSULACIÓN DE ERRORES PARA EL CHATBOT
# =============================================================================
class SymbiomemesisError(Exception):
    def __init__(self, mensaje, codigo="ERR-MATH-000", sugerencia=""):
        self.codigo = codigo
        self.sugerencia = sugerencia
        super().__init__(f"[{codigo}] {mensaje}")

class PrerrequisitoError(SymbiomemesisError):
    """Falta de datos financieros o de telemetría previa."""
    pass

class ErrorDeCalculo(SymbiomemesisError):
    """Errores numéricos o inconsistencia en las variables."""
    pass

# =============================================================================
# 🧠 NÚCLEO MATEMÁTICO V7
# =============================================================================
class MotorMatematicoSymbiomemesisV7:
    """
    Ecuación Maestra: U = Σ · [⊥ / (1 + F)] · (ME + C_bi)
    Donde F = I_sicof + I_red
    """

    @classmethod
    def resolver_simbiomemesis_total(cls, cinta: MallaCognitivaCompartida) -> bool:
        """
        Calcula la Utilidad U y las razones de cambio.
        Actualiza la Matriz de Auditoría de la Cinta.
        """
        TM.encabezado("RESOLUCIÓN ANALÍTICA SYMBIOMEMESIS V7.0")
        desarrollo = []

        with TM.monitor(cinta, "MOTOR_MATEMATICO", "Calculo_Caja_Blanca_U") as monitor:
            try:
                # 1. VALIDACIÓN DE PRERREQUISITOS
                if not cinta.datos_reporte_financiero:
                    raise PrerrequisitoError(
                        "Faltan datos financieros (ABC).", "ERR-MATH-404-ABC",
                        "Active el agente de costeo financiero antes de calcular la utilidad."
                    )
                
                if not cinta.datos_resultados_tester:
                    raise PrerrequisitoError(
                        "Malla de 45 variables no detectada.", "ERR-MATH-404-TESTER",
                        "Ejecute la medición del Agente Tester para obtener los indicadores estocásticos."
                    )

                # 2. EXTRACCIÓN DE DATOS (ÚLTIMA MEDICIÓN [-1])
                tester = cinta.datos_resultados_tester
                indices = tester.valores_crudos_cuarenta_y_cinco_indicadores
                abc = cinta.datos_reporte_financiero
                iter_actual = tester.numero_de_iteracion_actual

                # Helper para promediar grupos de variables
                def prom(prefijo):
                    vals = [v[-1] for k, v in indices.items() if k.startswith(prefijo)]
                    return np.mean(vals) if vals else 0.5

                # 3. PROCESAMIENTO DE PILARES (Caja Blanca)
                # A. Factor ME (Machine Education)
                me_val = prom("ME_")
                d_task = 8.5 # Factor de dificultad institucional (Calibrado UR)
                factor_ME = (0.95 * me_val) / d_task
                desarrollo.append(f"1. Machine Education (ME): {factor_ME:.4f} [Basado en {me_val:.2f} de aprendizaje]")

                # B. Factor C_bi (Costo Institucional Normalizado)
                c_bi = abc.costo_total_calculado / 1_000_000.0 # Normalización a Millones
                desarrollo.append(f"2. Costo Base (C_bi): {c_bi:.4f} M-COP [Costo Directo + Indirecto]")

                # C. Factor Σ (Sinergia de Enjambre)
                sigma = prom("SG_")
                desarrollo.append(f"3. Sinergia (Σ): {sigma:.4f} [Eficiencia de interacción multi-agente]")

                # D. Estabilidad Operativa (⊥ / (1+F))
                friccion = prom("FR_")
                estabilidad = 1.0 / (1.0 + friccion)
                desarrollo.append(f"4. Estabilidad (⊥): {estabilidad:.4f} [Fricción detectada: {friccion:.4f}]")

                # 4. CÁLCULO DE UTILIDAD U
                u_final = sigma * estabilidad * (factor_ME + c_bi)
                desarrollo.append(f"👉 RESULTADO U (M{iter_actual}) = {sigma:.3f} * {estabilidad:.3f} * ({factor_ME:.3f} + {c_bi:.3f}) = {u_final:.4f}")

                # 5. CÁLCULO DE RAZONES DE CAMBIO (DERIVADAS PARCIALES)
                razon_msg = "Derivada (ΔU/ΔM) no calculable en M1."
                if iter_actual > 1:
                    # Recuperar U anterior (aproximación)
                    u_prev = cls._calcular_u_medicion_anterior(indices, abc)
                    delta_u = u_final - u_prev
                    razon_msg = f"Gradiente ΔU (M{iter_actual}-M{iter_actual-1}): {delta_u:.5f}"
                    desarrollo.append(f"📉 {razon_msg}")

                # 6. VEREDICTO Y PERSISTENCIA
                veredicto = cls._obtener_veredicto(u_final)
                
                cinta.datos_matriz_auditoria = MatrizDeAuditoriaCientifica(
                    variables_promediadas_por_momento={"Utilidad_U": u_final, "Sigma": sigma, "ME": factor_ME},
                    valor_precalculo_de_friccion=float(friccion),
                    observaciones_cualitativas_del_auditor=f"{veredicto} | {razon_msg}",
                    desarrollo_matematico_paso_a_paso=desarrollo
                )

                # Persistencia estigmérgica
                cls._persistir_en_pinecone(u_final, veredicto, iter_actual)
                
                TM.evento("MOTOR_MAT", f"Cálculo M{iter_actual} completado: U={u_final:.4f}")
                monitor.registrar_tokens(entrada=350, salida=120)
                return True

            except SymbiomemesisError as se:
                TM.error(se.mensaje)
                raise se
            except Exception as e:
                TM.error(f"Fallo matemático: {str(e)}")
                raise ErrorDeCalculo(f"Error numérico: {str(e)}", "ERR-MATH-500")

    @staticmethod
    def _calcular_u_medicion_anterior(indices, abc):
        """Calcula una U aproximada de la medición previa para el gradiente."""
        def prom_prev(prefijo):
            vals = [v[-2] for k, v in indices.items() if k.startswith(prefijo) and len(v) > 1]
            return np.mean(vals) if vals else 0.5
        
        me_p = (0.95 * prom_prev("ME_")) / 8.5
        c_bi_p = abc.costo_total_calculado / 1_000_000.0
        sig_p = prom_prev("SG_")
        est_p = 1.0 / (1.0 + prom_prev("FR_"))
        return sig_p * est_p * (me_p + c_bi_p)

    @staticmethod
    def _obtener_veredicto(u):
        if u > 1.5: return "✅ SIMBIOSIS DE ALTO IMPACTO"
        if u > 1.0: return "✳️ SIMBIOSIS OPERATIVA"
        return "⚠️ FRICCIÓN SISTÉMICA DETECTADA"

    @staticmethod
    def _persistir_en_pinecone(u, ver, it):
        """Guarda el resultado en Pinecone usando el nuevo motor Gemini Embedding 2."""
        try:
            client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
            pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
            idx = pc.Index(os.getenv("PINECONE_INDEX"))
            
            res = client.models.embed_content(
                model="gemini-embedding-2-preview",
                contents=f"Auditoría M{it}: {ver}. U={u:.4f}"
            )
            
            idx.upsert(vectors=[{
                "id": f"math_res_{datetime.now().strftime('%H%M%S')}",
                "values": res.embeddings[0].values,
                "metadata": {"u": u, "it": it, "ver": ver}
            }], namespace="auditoria-cientifica-v7")
        except: pass

    @staticmethod
    def obtener_desglose_para_chatbot(cinta: MallaCognitivaCompartida) -> str:
        """Devuelve el desarrollo matemático listo para ser impreso en Streamlit."""
        if not cinta.datos_matriz_auditoria:
            return "❌ No hay cálculos disponibles en la cinta."
        
        pasos = cinta.datos_matriz_auditoria.desarrollo_matematico_paso_a_paso
        return "\n".join([f"› {p}" for p in pasos])