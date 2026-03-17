"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Agente Generador de Arsenal con Consolidación Excel (v8.0)
UBICACIÓN: /FIS_VERSION8/
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Evolución del generador v7. Implementa:
    1. Consolidación de Caja Blanca en un único archivo .xlsx.
    2. Compatibilidad con la Fábrica de Agentes v8.
    3. Manejo de rutas desde subcarpeta FIS_VERSION8.
=============================================================================
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional

# Añadir el directorio raíz al PATH para poder importar la telemetría v7
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from fis_telemetria_v7 import TelemetriaMaestraV7 as TM
except ImportError:
    class TM:
        @staticmethod
        def evento(a, m, c=""): print(f"[{a}] {m}")
        @staticmethod
        def encabezado(t): print(f"\n=== {t} ===")

class ArsenalError(Exception): pass

class AgenteGeneradorFisV8:
    """
    Arquitecto de Datos v8.0.
    Genera CSVs y un Libro Mayor en Excel para Auditoría Forense.
    """
    
    def __init__(self, raw_data_path="../data", output_dir="../ORIGENDATOS"):
        # Ajuste de rutas para salir de FIS_VERSION8 y encontrar carpetas raíz
        self.output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), output_dir))
        self.raw_path = os.path.abspath(os.path.join(os.path.dirname(__file__), raw_data_path))
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.ruta_excel_fuente = os.path.join(self.raw_path, "OFERTA ACADEMICA ASIGNATURAS 2024.xlsx")
        if not os.path.exists(self.ruta_excel_fuente):
            raise ArsenalError(f"Fuente Maestra no encontrada en: {self.ruta_excel_fuente}")
            
        self.df_maestro = pd.read_excel(self.ruta_excel_fuente, sheet_name="ClasificaAsignaturas2024UR")

    def ejecutar_plan_total(self, cinta: Any, **kwargs) -> str:
        """Punto de entrada compatible con la Fábrica de Agentes."""
        f_sel = kwargs.get('facultades_sel', [])
        p_sel = kwargs.get('programas_sel', [])
        asig_sel = kwargs.get('asignaturas_sel', [])

        TM.encabezado("GÉNESIS DE ARSENAL V8.0 - ESTRUCTURA DE CARPETAS")
        
        df_f = self.df_maestro.copy()
        if f_sel: df_f = df_f[df_f['FACULTAD_ASIGNATURA'].isin(f_sel)]
        if p_sel: df_f = df_f[df_f['NOMBRE_PROGRAMA'].isin(p_sel)]
        if asig_sel: df_f = df_f[df_f['NOMBRE_ASIGNATURA'].isin(asig_sel)]

        if df_f.empty:
            return "ALERTA: Sin datos para procesar."

        lista_asigs = df_f['NOMBRE_ASIGNATURA'].dropna().unique().tolist()
        
        # Generación de componentes
        df_doc = self._fabricar_docentes(lista_asigs)
        df_sw  = self._fabricar_software()
        df_hab = self._fabricar_habitat()
        df_act, costo_dir_total = self._fabricar_actividades(df_doc, df_hab, df_sw)
        df_admin = self._fabricar_admin(costo_dir_total)
        
        # Consolidación Excel (Caja Blanca)
        ruta_excel = self._generar_consolidado_maestro(df_act, df_doc, df_hab, df_sw, df_admin, df_f)

        return f"v8.0: Arsenal Fabricado y Consolidado en {os.path.basename(ruta_excel)}"

    def _fabricar_docentes(self, asignaturas):
        datos = [{"ID_Docente": f"DOC-v8-{i:03}", "Asignatura": asig, "Valor_Hora": 225000} for i, asig in enumerate(asignaturas)]
        df = pd.DataFrame(datos)
        df.to_csv(os.path.join(self.output_dir, f"maestro_docentes_v8_{self.timestamp}.csv"), index=False)
        return df

    def _fabricar_software(self):
        df = pd.DataFrame({"ID_Bundle": ["SW-v8-IA", "SW-v8-NONE"], "Costo_Hr": [15000, 0]})
        df.to_csv(os.path.join(self.output_dir, f"maestro_software_v8_{self.timestamp}.csv"), index=False)
        return df

    def _fabricar_habitat(self):
        df = pd.DataFrame([{"ID_Sala": f"SALA-v8-{i}", "M2": 50, "Costo_M2_Hr": 600} for i in range(5)])
        df.to_csv(os.path.join(self.output_dir, f"maestro_habitat_v8_{self.timestamp}.csv"), index=False)
        return df

    def _fabricar_actividades(self, df_doc, df_hab, df_sw):
        datos = []
        for _, doc in df_doc.iterrows():
            datos.append({
                "ID_Docente": doc['ID_Docente'], "Asignatura": doc['Asignatura'],
                "ID_Sala": "SALA-v8-1", "M2": 50, "Valor_Hora_Doc": doc['Valor_Hora'],
                "Costo_Habitat_Hr": 30000, "Costo_Software_Hr": 15000, "Horas_Sesion": 3
            })
        df = pd.DataFrame(datos)
        total_d = (df['Valor_Hora_Doc'].sum() + df['Costo_Habitat_Hr'].sum()) * 3
        df.to_csv(os.path.join(self.output_dir, f"registro_actividades_v8_{self.timestamp}.csv"), index=False)
        return df, total_d

    def _fabricar_admin(self, total_d):
        df = pd.DataFrame([{"Bolsa_Indirecta": total_d * 0.40}])
        df.to_csv(os.path.join(self.output_dir, f"maestro_admin_v8_{self.timestamp}.csv"), index=False)
        return df

    def _generar_consolidado_maestro(self, df_act, df_doc, df_hab, df_sw, df_admin, df_f):
        path = os.path.join(self.output_dir, f"CONSOLIDADO_ABC_v8_{self.timestamp}.xlsx")
        df_final = df_act.merge(df_f[['NOMBRE_ASIGNATURA', 'NOMBRE_PROGRAMA']].drop_duplicates(), 
                                left_on='Asignatura', right_on='NOMBRE_ASIGNATURA', how='left')
        
        # Prorrateo simple para el consolidado
        ind_u = df_admin['Bolsa_Indirecta'].iloc[0] / len(df_act)
        df_final['Costo_Indirecto'] = ind_u
        df_final['Costo_Total_Clase'] = (df_final['Valor_Hora_Doc'] * 3) + ind_u

        with pd.ExcelWriter(path, engine='openpyxl') as writer:
            df_final.to_excel(writer, sheet_name='LIQUIDACION_v8', index=False)
        return path