"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v7.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Script de Prueba - FASE 2 (Sincronización de Costeo ABC)
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
=============================================================================
"""

import os
import sys
from datetime import datetime

# Importación de los componentes del núcleo V7
from fis_cintagentica_v7 import MallaCognitivaCompartida
from fis_calculaCostosABC_V7 import MotorDeCosteoFinancieroABC_V7
from fis_informe_v7 import GeneradorReporteV7

# Configuración de Consola
class Consola:
    @staticmethod
    def titulo(m): print(f"\n{'='*70}\n{m}\n{'='*70}")
    @staticmethod
    def info(m): print(f"[*] {m}")
    @staticmethod
    def exito(m): print(f"✅ {m}")
    @staticmethod
    def error(m): print(f"❌ {m}")

def ejecutar_test_fase2():
    Consola.titulo("TEST DE INTEGRACIÓN: FASE 2 - LIQUIDACIÓN FINANCIERA ABC")

    # 1. Inicializar la Malla Cognitiva
    cinta = MallaCognitivaCompartida()
    cinta.inicializar_auditoria_financiera()
    Consola.info("Malla Cognitiva conectada y TRM actualizada.")

    # 2. Ejecutar el Motor Financiero (Método Estático V7)
    Consola.info("Iniciando Motor de Costeo Financiero ABC_V7...")
    
    try:
        # Llamamos al método correcto definido en fis_calculaCostosABC_V7.py
        exito_calculo = MotorDeCosteoFinancieroABC_V7.ejecutar_calculo_de_costos_abc(cinta)
        
        if exito_calculo:
            rep = cinta.datos_reporte_financiero
            Consola.exito(f"Liquidación finalizada: ${rep.costo_total_calculado:,.2f} COP")
        else:
            Consola.error("El motor financiero devolvió un fallo lógico.")
            return

    except Exception as e:
        Consola.error(f"Error crítico en el flujo de cálculo: {e}")
        return

    # 3. Disparar Generación de Informe PDF (Renderizado Institucional)
    Consola.info("Iniciando renderizado del Informe Científico PDF...")
    try:
        # Nota: Asegúrate de que GeneradorReporteV7 use el método generar_pdf(cinta)
        ruta_pdf = GeneradorReporteV7.generar_pdf(cinta)
        Consola.exito(f"Proceso completo. Reporte disponible en: {ruta_pdf}")
    except Exception as e:
        Consola.error(f"Error generando el PDF: {e}")

if __name__ == "__main__":
    ejecutar_test_fase2()