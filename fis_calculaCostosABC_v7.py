"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v7.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Motor de Costeo Financiero (Activity Based Costing - ABC)
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Núcleo de liquidación financiera. Integra el arsenal de datos CSV
    para determinar el costo total (Directo + Indirecto).
    Incluye Telemetría Maestra y Auditoría de Integridad de Datos.
=============================================================================
"""

import os
import pandas as pd
import glob
from typing import Dict, Optional
from fis_cintagentica_v7 import MallaCognitivaCompartida, ReporteFinancieroCosteoDeClase
from fis_telemetria_v7 import TelemetriaMaestraV7 as TM

# --- ENCAPSULACIÓN DE ERRORES FINANCIEROS ---
class FinanzasError(Exception):
    """Errores específicos de la liquidación ABC."""
    def __init__(self, mensaje, codigo="ERR-FIN-000"):
        self.codigo = codigo
        super().__init__(f"[{codigo}] {mensaje}")

class MotorDeCosteoFinancieroABC_V7:
    """
    Implementa el modelo ABC V7 con trazabilidad forense.
    Realiza el cruce de maestros y el prorrateo de costos indirectos.
    """

    @staticmethod
    def _encontrar_archivo_reciente(directorio: str, patron: str) -> str:
        """Localiza el arsenal más reciente generado por el Agente Generador."""
        archivos = glob.glob(os.path.join(directorio, f"{patron}_*.csv"))
        if not archivos:
            raise FinanzasError(f"Falta el archivo maestro: {patron}", "ERR-FIN-404")
        return max(archivos)

    @classmethod
    def ejecutar_calculo_de_costos_abc(cls, cinta: MallaCognitivaCompartida) -> bool:
        """
        Orquesta la liquidación financiera y actualiza la Malla Cognitiva.
        """
        TM.encabezado("CONSOLIDACIÓN FINANCIERA ABC V7.0")
        
        with TM.monitor(cinta, "MOTOR_FINANCIERO", "Liquidacion_ABC_Total") as monitor:
            directorio_datos = "ORIGENDATOS"
            
            try:
                # 1. CARGA DE ARSENAL
                TM.evento("FINANZAS", "Cargando arsenal de datos desde 'ORIGENDATOS'...")
                df_act = pd.read_csv(cls._encontrar_archivo_reciente(directorio_datos, "registro_actividades_clase"))
                df_doc = pd.read_csv(cls._encontrar_archivo_reciente(directorio_datos, "maestro_docentes"))
                df_hab = pd.read_csv(cls._encontrar_archivo_reciente(directorio_datos, "maestro_habitat_detallado"))
                df_sw  = pd.read_csv(cls._encontrar_archivo_reciente(directorio_datos, "maestro_software"))
                df_adm = pd.read_csv(cls._encontrar_archivo_reciente(directorio_datos, "maestro_admin_detallado"))

                # 2. CÁLCULO DE TASA INDIRECTA (PRORRATEO)
                TM.evento("FINANZAS", "Calculando bolsa administrativa e indirectos...")
                cols_admin = [
                    "Costo_Nomina_Admin", "Costo_Servicios_Centrales", 
                    "Costo_Soporte_IA_Symbiomemesis"
                ]
                bolsa_admin = df_adm[cols_admin].sum(axis=1).iloc[0]
                factor_abc  = df_adm["Factor_Distribucion_ABC"].iloc[0]
                total_horas = df_adm["Total_Horas_Inst"].iloc[0]
                
                # Tasa horaria de indirectos
                tasa_indirecta_hr = (bolsa_admin * factor_abc) / total_horas

                # 3. INTEGRACIÓN (MERGING) Y VALIDACIÓN DE CAJA BLANCA
                df_m = pd.merge(df_act, df_doc, on="ID_Docente", how="left")
                df_m = pd.merge(df_m, df_hab, on="ID_Sala", how="left")
                df_m = pd.merge(df_m, df_sw, on="ID_Bundle", how="left")

                # Verificación de integridad: ¿Quedaron NAs tras el cruce?
                if df_m[['Valor_Hora_COP', 'Metros_Cuadrados']].isnull().values.any():
                    raise FinanzasError("Inconsistencia en cruce de datos (IDs huérfanos detectados).", "ERR-FIN-002")

                # 4. CÁLCULO DE RUBROS ESPECÍFICOS
                # A. Docencia Directa
                df_m['C_Docencia'] = df_m['Valor_Hora_COP'] * df_m['Horas']
                
                # B. Hábitat (Mantenimiento, Servicios, Depreciación...)
                rubros_hab = [
                    "Costo_Mantenimiento_Hr", "Costo_Aseo_Seguridad_Hr", 
                    "Costo_Servicios_Publicos_Hr", "Costo_Depreciacion_Hr"
                ]
                df_m['C_Habitat'] = df_m[rubros_hab].sum(axis=1) * df_m['Horas']
                
                # C. Software especializado
                df_m['C_Software'] = (df_m['Costo_Hr_Estudiante'] * df_m['Alumnos']) * df_m['Horas']
                
                # D. Indirecto ABC
                df_m['C_Indirecto'] = tasa_indirecta_hr * df_m['Horas']

                # 5. CONSOLIDACIÓN FINAL
                tot_doc = df_m['C_Docencia'].sum()
                tot_hab = df_m['C_Habitat'].sum()
                tot_sw  = df_m['C_Software'].sum()
                tot_ind = df_m['C_Indirecto'].sum()
                costo_total = tot_doc + tot_hab + tot_sw + tot_ind

                reporte = {
                    "Directo_Docencia_COP": round(tot_doc, 2),
                    "Directo_Habitat_COP": round(tot_hab, 2),
                    "Directo_Software_COP": round(tot_sw, 2),
                    "Indirecto_Administrativo_COP": round(tot_ind, 2),
                    "Tasa_Prorrateo_Hr": round(tasa_indirecta_hr, 4)
                }

                # 6. ACTUALIZACIÓN DE LA MALLA COGNITIVA
                cinta.datos_reporte_financiero = ReporteFinancieroCosteoDeClase(
                    costo_total_calculado=round(costo_total, 2),
                    desglose_de_costos_por_categoria=reporte
                )

                cinta.registrar_evento_forense_detallado(
                    emisor="MOTOR_FINANCIERO",
                    receptor="AUDITOR_FORENSE",
                    mensaje=f"Liquidación Exitosa: ${costo_total:,.2f} COP.",
                    resultado=str(reporte)
                )

                TM.info_financiera(f"Costeo finalizado con éxito. Total: ${costo_total:,.2f} COP")
                monitor.registrar_tokens(entrada=100, salida=150) # Metadatos de control
                return True

            except FinanzasError as fe:
                TM.error(f"Fallo en motor financiero: {fe.mensaje}")
                raise fe
            except Exception as e:
                msg = f"Error no controlado en cálculo ABC: {str(e)}"
                TM.error(msg)
                raise FinanzasError(msg, "ERR-FIN-500")

# =============================================================================
# PRUEBA STANDALONE
# =============================================================================
if __name__ == "__main__":
    from fis_cintagentica_v7 import MallaCognitivaCompartida
    print("🧠 Iniciando Test del Motor Financiero ABC...")
    cinta_test = MallaCognitivaCompartida()
    cinta_test.inicializar_auditoria_financiera()
    
    if MotorDeCosteoFinancieroABC_V7.ejecutar_calculo_de_costos_abc(cinta_test):
        res = cinta_test.datos_reporte_financiero
        print(f"\n✅ REPORTE GENERADO: ${res.costo_total_calculado:,.2f} COP")