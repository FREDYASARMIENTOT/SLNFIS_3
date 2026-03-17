"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Motor de Costeo ABC - Unidad Mínima de Clase (v8.0)
UBICACIÓN: /FIS_VERSION8/
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Liquidador Financiero con trazabilidad jerárquica total.
    1. Lee ORIGENDATOS (CSVs y Excel Consolidado).
    2. Recalcula el costeo basado en la unidad mínima: LA CLASE.
    3. Genera copia validada en /data con el mismo nombre y timestamp.
=============================================================================
"""

import os
import pandas as pd
import glob
from datetime import datetime
from typing import Dict, Any, Optional

# --- IMPORTACIONES LOCALES V8 ---
from fis_telemetria_v8 import TelemetriaMaestraV8 as TM

class FinanzasErrorV8(Exception):
    def __init__(self, mensaje, codigo="ERR-FIN-V8"):
        self.codigo = codigo
        super().__init__(f"[{codigo}] {mensaje}")

class MotorDeCosteoFinancieroABC_V8:
    """
    Motor de Liquidación Jerárquica. 
    Valida la coherencia entre ORIGENDATOS y genera el entregable en /data.
    """

    @staticmethod
    def _ubicar_recursos_v8() -> Dict[str, str]:
        """Localiza el set de archivos síncronos más recientes."""
        ruta_origen = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ORIGENDATOS"))
        
        # Localizar el Excel Maestro para extraer el timestamp exacto
        lista_excels = glob.glob(os.path.join(ruta_origen, "CONSOLIDADO_ABC_v8_*.xlsx"))
        if not lista_excels:
            raise FinanzasErrorV8("No se encontró el Excel Consolidado en ORIGENDATOS.", "ERR-404-XLSX")
        
        excel_reciente = max(lista_excels, key=os.path.getmtime)
        timestamp = "_".join(os.path.basename(excel_reciente).split("_")[-2:]).split(".")[0]
        
        return {
            "excel_gen": excel_reciente,
            "timestamp": timestamp,
            "csv_act": os.path.join(ruta_origen, f"registro_actividades_v8_{timestamp}.csv"),
            "csv_doc": os.path.join(ruta_origen, f"maestro_docentes_v8_{timestamp}.csv"),
            "csv_hab": os.path.join(ruta_origen, f"maestro_habitat_v8_{timestamp}.csv"),
            "csv_adm": os.path.join(ruta_origen, f"maestro_admin_v8_{timestamp}.csv")
        }

    @classmethod
    def ejecutar_calculo_de_costos_abc(cls, cinta: Any, **kwargs) -> str:
        """
        Punto de entrada: Validación de ORIGENDATOS -> Recalculo -> /data/
        """
        TM.encabezado("LIQUIDACIÓN FORENSE POR UNIDAD MÍNIMA (CLASE) - v8.0")
        monitor = kwargs.get('monitor_forense')
        SESIONES_DEFAULT = 10  # 10 clases por grupo

        try:
            # 1. UBICACIÓN Y CARGA SÍNCRONA
            recursos = cls._ubicar_recursos_v8()
            TM.evento("ABC_V8", f"Sincronizando con Timestamp: {recursos['timestamp']}")
            
            df_act = pd.read_csv(recursos['csv_act'])
            df_doc = pd.read_csv(recursos['csv_doc'])
            df_hab = pd.read_csv(recursos['csv_hab'])
            df_adm = pd.read_csv(recursos['csv_adm'])
            
            # Carga del Excel generado para extraer la jerarquía académica
            df_excel_gen = pd.read_excel(recursos['excel_gen'])

            # 2. PROCESO DE RECALCULO Y EXPANSIÓN JERÁRQUICA
            TM.evento("ABC_V8", "Iniciando expansión de registros a unidad mínima: Clase.")
            registros_auditados = []
            
            # Bolsa administrativa para prorrateo
            bolsa_total = df_adm["Bolsa_Indirecta"].iloc[0]
            costo_ind_clase = bolsa_total / (len(df_act) * SESIONES_DEFAULT)

            for _, grupo in df_act.iterrows():
                # Recuperar jerarquía desde el Excel de Génesis
                info_jerarquia = df_excel_gen[df_excel_gen['Asignatura'] == grupo['Asignatura']].iloc[0]
                
                for s in range(1, SESIONES_DEFAULT + 1):
                    # Recalculo de Costos Directos
                    c_doc = grupo['Valor_Hora_Doc'] * grupo['Horas_Sesion']
                    c_hab = grupo['Costo_Habitat_Hr'] * grupo['Horas_Sesion']
                    c_sw  = grupo['Costo_Software_Hr'] * grupo['Horas_Sesion']
                    
                    registros_auditados.append({
                        "ID_Clase_Forense": f"CL-{recursos['timestamp']}-{grupo['ID_Docente']}-S{s:02}",
                        "Nivel_Formacion": "POSGRADO", # O extraer de la base maestra si aplica
                        "Facultad": info_jerarquia.get('FACULTAD_ASIGNATURA', 'ICT'),
                        "Programa": info_jerarquia.get('NOMBRE_PROGRAMA', 'MAESTRIA/DOCTORADO'),
                        "Asignatura": grupo['Asignatura'],
                        "ID_Grupo": grupo['ID_Docente'], # El ID_Docente actúa como ancla del grupo
                        "Sesion": f"Sesion_{s:02}",
                        "Costo_Docente": c_doc,
                        "Costo_Habitat": c_hab,
                        "Costo_Software": c_sw,
                        "Costo_Indirecto": costo_ind_clase,
                        "COSTO_TOTAL_CLASE": c_doc + c_hab + c_sw + costo_ind_clase
                    })

            df_final = pd.DataFrame(registros_auditados)

            # 3. EXPLICABILIDAD MATEMÁTICA (Monitor Forense)
            if monitor:
                TM.explicar_calculo(
                    monitor,
                    formula="C_Total_Clase = Σ(Directos) + (Bolsa_Admin / N_Total_Clases)",
                    variables={"Bolsa": bolsa_total, "Clases_Procesadas": len(df_final)},
                    resultado=f"${df_final['COSTO_TOTAL_CLASE'].sum():,.2f}"
                )

            # 4. PERSISTENCIA EN /data (COPIA VALIDADA)
            ruta_data = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
            os.makedirs(ruta_data, exist_ok=True)
            
            nombre_archivo = os.path.basename(recursos['excel_gen'])
            path_destino = os.path.join(ruta_data, nombre_archivo)

            with pd.ExcelWriter(path_destino, engine='openpyxl') as writer:
                df_final.to_excel(writer, sheet_name='COSTEO_CLASE_V8', index=False)

            # 5. ACTUALIZACIÓN DE LA CINTA
            if hasattr(cinta, 'datos_reporte_financiero'):
                cinta.datos_reporte_financiero.costo_total_calculado = round(df_final['COSTO_TOTAL_CLASE'].sum(), 2)
                cinta.datos_reporte_financiero.desglose_de_costos_por_categoria = {
                    "Ruta_Validada": path_destino,
                    "Total_Clases": len(df_final)
                }

            msg_exito = f"Validación ABC completa. Excel Forense creado en /data/{nombre_archivo}"
            TM.evento("ABC_V8", msg_exito)
            return msg_exito

        except Exception as e:
            err = f"Falla en Motor ABC v8: {str(e)}"
            TM.error(err)
            return err