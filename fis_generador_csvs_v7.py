"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v7.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Agente Generador Dinámico de Datos (ABC Costing)
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Genera el arsenal de archivos CSV para el costeo ABC.
    Basado en el Excel oficial de la UR. Implementa jerarquía multinivel,
    selección múltiple, reglas de negocio de costos directos/indirectos 
    y telemetría centralizada.
=============================================================================
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional, List, Dict
from contextlib import contextmanager

# --- INTEGRACIÓN CON EL SISTEMA DE TELEMETRÍA V7 ---
try:
    from fis_telemetria_v7 import TelemetriaMaestraV7 as TM
except ImportError:
    class TM:
        @staticmethod
        def encabezado(t): print(f"\n=== {t} ===")
        @staticmethod
        def evento(a, msg, color=""): print(f"[{a}] {msg}")
        @staticmethod
        def error(msg): print(f"[ERROR] {msg}")
        @staticmethod
        def info_financiera(msg): print(f"[FIN] {msg}")
        @staticmethod
        @contextmanager
        def monitor(cinta, agente, accion):
            yield type('obj', (object,), {'registrar_tokens': lambda a,b: None, 'registrar_accion_vectorial': lambda a: None})

# --- ENCAPSULACIÓN DE ERRORES PARA EL CHATBOT ---
class ArsenalError(Exception):
    def __init__(self, mensaje, codigo="ERR-ARS-000"):
        self.codigo = codigo
        super().__init__(f"[{codigo}] {mensaje}")

class AgenteGeneradorFisV7:
    """
    Agente Orquestador del Arsenal de Datos.
    Gestiona la lógica de filtrado jerárquico y fabricación de registros.
    """
    
    def __init__(self, raw_data_path="./data", output_dir="ORIGENDATOS"):
        self.output_dir = output_dir
        self.raw_path = raw_data_path
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        self.cinta = None 
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Carga de la fuente maestra (Excel 2024 UR)
        self.ruta_excel = os.path.join(self.raw_path, "OFERTA ACADEMICA ASIGNATURAS 2024.xlsx")
        if not os.path.exists(self.ruta_excel):
            raise ArsenalError(f"No se encontró la base maestra en: {self.ruta_excel}", "ERR-ARS-404")
            
        try:
            self.df_clasificacion = pd.read_excel(self.ruta_excel, sheet_name="ClasificaAsignaturas2024UR")
        except Exception as e:
            raise ArsenalError(f"Error al leer la estructura del Excel: {str(e)}", "ERR-ARS-500")

    def _get_path(self, name):
        return os.path.join(self.output_dir, f"{name}_{self.timestamp}.csv")

    def ejecutar_plan_total(self, cinta, facultades_solicitadas: List[str] = None, 
                            programas_solicitados: List[str] = None, 
                            asignaturas_solicitadas: List[str] = None):
        """
        Punto de entrada principal. Filtra jerárquicamente:
        Facultad (Abuelo) -> Programa (Padre) -> Asignatura (Hijo).
        """
        self.cinta = cinta
        TM.encabezado("GÉNESIS DE ARSENAL DE DATOS V7.0")

        with TM.monitor(self.cinta, "AGENTE_GENERADOR", "Fabricacion_Arsenal_CSV") as monitor:
            
            # 1. FILTRADO JERÁRQUICO MULTINIVEL
            df_f = self.df_clasificacion.copy()
            
            # A. Filtro Facultad (Abuelo)
            if facultades_solicitadas:
                df_f = df_f[df_f['FACULTAD_ASIGNATURA'].isin(facultades_solicitadas)]
            
            # B. Filtro Programa (Padre)
            if programas_solicitados:
                df_f = df_f[df_f['NOMBRE_PROGRAMA'].isin(programas_solicitados)]
            
            # C. Filtro Asignatura (Hijo)
            if asignaturas_solicitadas:
                df_f = df_f[df_f['NOMBRE_ASIGNATURA'].isin(asignaturas_solicitadas)]

            if df_f.empty:
                raise ArsenalError("La combinación de filtros no arrojó resultados en el Excel.", "ERR-ARS-001")

            lista_asigs = df_f['NOMBRE_ASIGNATURA'].dropna().unique().tolist()
            TM.evento("GENERADOR", f"Detectadas {len(lista_asigs)} entidades académicas bajo los filtros.")

            # 2. GENERACIÓN SECUENCIAL BASADA EN REGLAS DE NEGOCIO
            df_doc = self._fabricar_docentes(lista_asigs)
            df_sw  = self._fabricar_software()
            df_hab = self._fabricar_habitat()
            
            # 3. CÁLCULO DE COSTO DIRECTO Y ACTIVIDADES
            costo_directo_total = self._fabricar_registro_actividades(df_doc, df_hab, df_sw)
            
            # 4. GESTIÓN DE COSTO INDIRECTO (Regla del < 50%)
            self._fabricar_admin(costo_directo_total)

            # 5. VALIDACIÓN DE CAJA BLANCA
            self._validar_integridad()
            
            monitor.registrar_tokens(950, 500)
            TM.evento("GENERADOR", "Arsenal completo y validado para costeo ABC.")

    def _fabricar_docentes(self, asignaturas: list) -> pd.DataFrame:
        """Crea maestros de docentes con tarifas realistas por nivel posgrado."""
        datos = []
        for i, asig in enumerate(asignaturas):
            n_grupos = np.random.randint(1, 4) # 1 a 3 grupos por asignatura
            for g in range(n_grupos):
                datos.append({
                    "ID_Docente": f"DOC-{self.timestamp}-{i:03}-{g}",
                    "Asignatura_Principal": asig,
                    "Nivel_Formacion": "Doctorado/Maestría",
                    "Tipo_Vinculacion": np.random.choice(["Planta", "Cátedra"], p=[0.5, 0.5]),
                    "Valor_Hora_COP": np.random.choice([185000, 215000, 240000, 285000])
                })
        df = pd.DataFrame(datos)
        df.to_csv(self._get_path("maestro_docentes"), index=False)
        return df

    def _fabricar_software(self) -> pd.DataFrame:
        """Maestro de licenciamiento y bundles tecnológicos."""
        df = pd.DataFrame({
            "ID_Bundle": ["SW-IA-AVANZADO", "SW-ESTADISTICA", "SW-BASICO", "SIN-SW"],
            "Descripcion": ["Cloud GPU + Python API", "Stata + SPSS + Matlab", "Office 365", "Ninguno"],
            "Costo_Hr_Estudiante": [9200, 4800, 1200, 0]
        })
        df.to_csv(self._get_path("maestro_software"), index=False)
        return df

    def _fabricar_habitat(self) -> pd.DataFrame:
        """Cálculo de hábitat basado en m2."""
        datos = []
        for i in range(1, 16):
            m2 = np.random.randint(25, 90) # Espacios de 25 a 90 m2
            tipo = np.random.choice(["Lab_Informatica", "Aula_Teorica", "Sala_Doctorado"])
            
            # Reglas de costo basadas en el m2
            mantenimiento = m2 * 150 if "Lab" in tipo else m2 * 80
            aseo = m2 * 100
            servicios = m2 * 130 if "Lab" in tipo else m2 * 60
            
            datos.append({
                "ID_Sala": f"UR-SPACE-{i:03}",
                "Tipo_Espacio": tipo,
                "Metros_Cuadrados": m2,
                "Costo_Mantenimiento_Hr": mantenimiento,
                "Costo_Aseo_Seguridad_Hr": aseo,
                "Costo_Servicios_Publicos_Hr": servicios,
                "Costo_Depreciacion_Hr": m2 * 250,
                "Costo_Coord_Aula_Hr": 4500
            })
        df = pd.DataFrame(datos)
        df.to_csv(self._get_path("maestro_habitat_detallado"), index=False)
        return df

    def _fabricar_registro_actividades(self, df_doc, df_hab, df_sw) -> float:
        """Cruce de actividades para determinar el Costo Directo de Referencia."""
        datos = []
        total_directo = 0.0
        salas = df_hab['ID_Sala'].tolist()
        bundles = df_sw['ID_Bundle'].tolist()

        for _, doc in df_doc.iterrows():
            sala_id = np.random.choice(salas)
            sw_id = np.random.choice(bundles)
            n_alumnos = np.random.randint(8, 26)
            horas = 3
            sesiones = 12 # 12 sesiones por semestre

            # Sumatoria de costo docente para balanceo
            total_directo += (doc['Valor_Hora_COP'] * horas * sesiones)

            for s in range(1, sesiones + 1):
                datos.append({
                    "Periodo": "2025-1S",
                    "ID_Docente": doc['ID_Docente'],
                    "Asignatura": doc['Asignatura_Principal'],
                    "Sesion": s,
                    "ID_Sala": sala_id,
                    "ID_Bundle": sw_id,
                    "Horas": horas,
                    "Alumnos": n_alumnos
                })
        
        pd.DataFrame(datos).to_csv(self._get_path("registro_actividades_clase"), index=False)
        return total_directo

    def _fabricar_admin(self, costo_directo_ref: float):
        """Regla de Oro: El costo indirecto no debe superar el 50% del costo directo."""
        # Calculamos una bolsa que sea exactamente el 40% del directo para seguridad de auditoría
        bolsa_indirecta = costo_directo_ref * 0.40
        
        df = pd.DataFrame([{
            "Periodo": "2025-1S",
            "Costo_Nomina_Admin": bolsa_indirecta * 0.6,
            "Costo_Servicios_Centrales": bolsa_indirecta * 0.3,
            "Costo_Soporte_IA_Symbiomemesis": bolsa_indirecta * 0.1,
            "Factor_Distribucion_ABC": 0.20, 
            "Total_Horas_Inst": 45000
        }])
        df.to_csv(self._get_path("maestro_admin_detallado"), index=False)
        TM.info_financiera(f"Bolsa Indirecta Equilibrada: ${bolsa_indirecta:,.2f} COP")

    def _validar_integridad(self):
        """Validación de Caja Blanca Post-Generación."""
        try:
            act = pd.read_csv(self._get_path("registro_actividades_clase"))
            doc = pd.read_csv(self._get_path("maestro_docentes"))
            hab = pd.read_csv(self._get_path("maestro_habitat_detallado"))
            
            if not set(act['ID_Docente']).issubset(set(doc['ID_Docente'])):
                raise ArsenalError("Error de integridad: Docentes huérfanos detectados.", "ERR-VAL-001")
            
            if not set(act['ID_Sala']).issubset(set(hab['ID_Sala'])):
                raise ArsenalError("Error de integridad: Salas no registradas detectadas.", "ERR-VAL-002")
                
            TM.evento("AUDITOR", "Integridad referencial validada al 100%.")
        except Exception as e:
            if isinstance(e, ArsenalError): raise e
            raise ArsenalError(f"Fallo en auditoría de datos: {str(e)}", "ERR-VAL-500")

# =============================================================================
# PRUEBA STANDALONE
# =============================================================================
if __name__ == "__main__":
    class MockCinta:
        def agregar_registro_de_telemetria(self, r): pass

    agente = AgenteGeneradorFisV7(raw_data_path="./data")
    # Prueba con multi-selección de ejemplo
    agente.ejecutar_plan_total(
        cinta=MockCinta(), 
        facultades_solicitadas=["ESCUELA DE INGENIERÍA, CIENCIA Y TECNOLOGÍA"],
        programas_solicitados=["DOCTORADO EN INGENIERÍA, CIENCIA Y TECNOLOGÍA"]
    )