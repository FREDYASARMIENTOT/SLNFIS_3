"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v7.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Human-In-The-Loop (HITL) - Gestión de Intervención Institucional
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Punto de control de gobernanza y auditoría científica. 
    Gestiona la validación de las 45 variables y la transición de estados.
    Soporta persistencia resiliente ante errores de cuota (429).
=============================================================================
"""

import time
import random
from typing import Dict, List, Any
from fis_telemetria_v7 import TelemetriaMaestraV7 as TM, ColoresUR
from fis_cintagentica_v7 import (
    MallaCognitivaCompartida, 
    RegistroDeTelemetriaDeAgente,
    ResultadosDelInstrumentoDelTester
)

class GestorDeIntervencionHumanaV7:
    """
    Garante de la Gobernanza Humana. 
    Implementa el 'Kill Switch' y el 'Aprobado de Calidad' para la Tesis.
    """

    @staticmethod
    def presentar_auditoria_v7(cinta: MallaCognitivaCompartida) -> bool:
        """
        Interfáz de Auditoría de Caja Blanca. 
        Retorna True para avanzar (SEGUIR) o False para re-calcular (MEDIR).
        """
        inicio_pausa = time.time()
        datos_tester = cinta.datos_resultados_tester

        if not datos_tester:
            TM.error("HITL: No se detectó la malla de indicadores en la Cinta.")
            return False

        # --- 1. RENDERIZADO DEL ESTADO FINANCIERO Y OPERATIVO ---
        TM.encabezado("AUDITORÍA DE GOBERNANZA - SYMBIOMEMESIS V7.0")
        
        costo_abc = getattr(cinta.datos_reporte_financiero, 'costo_total_calculado', 0.0)
        iteracion = datos_tester.numero_de_iteracion_actual

        print(f"{ColoresUR.AZUL_SIS}PROYECTO:  {ColoresUR.RESET}{cinta.identificador_proyecto}")
        print(f"{ColoresUR.CIAN_FIN}COSTO ABC: {ColoresUR.RESET}${costo_abc:,.2f} COP")
        print(f"{ColoresUR.AMARILLO_HITL}MEDICIÓN:  {ColoresUR.RESET}M{iteracion}")
        
        # --- 2. VISUALIZACIÓN DE LA MATRIZ DE 45 VARIABLES (RESUMEN) ---
        print("\n" + "═" * 85)
        header = f"{'Indicador de Tesis (Pilar)':<35} | {'Valor Base':^12} | {'Tendencia':^12} | {'Estado':^15}"
        print(f"{ColoresUR.NEGRITA}{header}{ColoresUR.RESET}")
        print("─" * 85)
        
        # Mostramos una muestra representativa de los pilares
        items = list(datos_tester.valores_crudos_cuarenta_y_cinco_indicadores.items())
        for var, vals in items[:15]: # Visualización de los primeros 15 por brevedad en consola
            actual = vals[-1]
            previo = vals[-2] if len(vals) > 1 else actual
            flecha = "▲" if actual > previo else ("▼" if actual < previo else "•")
            color_val = ColoresUR.VERDE_AG if actual > 0.7 else ColoresUR.AMARILLO_HITL
            
            print(f"🧬 {var[:32]:<32} | {previo:^12.4f} | {flecha} {actual:^9.4f} | {color_val}{'OPTIMIZADO' if actual > 0.7 else 'EN PROCESO'}{ColoresUR.RESET}")
        
        print("═" * 85)

        # --- 3. TOMA DE DECISIÓN DE GOBERNANZA ---
        print(f"\n{ColoresUR.NEGRITA}ESTACIÓN DE MANDO - Seleccione una acción:{ColoresUR.RESET}")
        print(f" [{ColoresUR.AMARILLO_HITL}1{ColoresUR.RESET}] **MEDIR (Iterar)**: Guardar rastro en Pinecone y solicitar re-cálculo estocástico.")
        print(f" [{ColoresUR.VERDE_AG}2{ColoresUR.RESET}] **SEGUIR (Avanzar)**: Aprobar indicadores y proceder a la resolución de Utilidad $U$.")
        
        while True:
            opcion = input(f"\n{ColoresUR.AMARILLO_HITL}👉 Comando (1 o 2): {ColoresUR.RESET}").strip()

            if opcion == "1":
                # MOMENTO 1: PERSISTENCIA Y RE-INTENTO
                TM.evento("HITL", "Iniciando protocolo de persistencia vectorial...")
                try:
                    cinta.registrar_evento_forense_detallado(
                        emisor="AUDITOR_HUMANO", 
                        receptor="MEMORIA_ESTIGMERGICA",
                        mensaje=f"Rechazo de M{iteracion}. Solicitando optimización de gradiente.",
                        entrada="Comando_MEDIR", salida="SYNC_VEC_DB"
                    )
                except Exception:
                    TM.error("Error 429: Cuota excedida. Persistiendo rastro en LOG local únicamente.")
                
                return False # Señal para que el orquestador repita el Tester

            elif opcion == "2":
                # MOMENTO 2: CLAUSURA OPERACIONAL
                duracion = time.time() - inicio_pausa
                TM.evento("HITL", "Cierre de auditoría detectado. Sincronizando Malla...")
                
                cinta.registrar_evento_forense_detallado(
                    emisor="AUDITOR_HUMANO", 
                    receptor="MOTOR_MATEMATICO",
                    mensaje=f"APROBACIÓN M{iteracion}. Bloqueando variables para cálculo de U.",
                    entrada="Comando_SEGUIR", salida="LOCK_STATE",
                    tiempo_reflexion=duracion
                )
                
                return True # Señal para avanzar a la fase matemática
            
            else:
                print(f"{ColoresUR.VINO}⚠️ Entrada no válida. Digite 1 (Medir) o 2 (Seguir).{ColoresUR.RESET}")

# =============================================================================
# 🧪 BUCLE DE SIMULACIÓN INTERACTIVA (TEST STANDALONE)
# =============================================================================
if __name__ == "__main__":
    # Inicialización de entorno de prueba
    cinta_mock = MallaCognitivaCompartida()
    cinta_mock.inicializar_auditoria_financiera()
    
    # Simulamos el arsenal de 45 variables
    vars_demo = {f"INDICADOR_{i:02}_VARIABLE_DESCRIPTIVA_LARGA": [0.5, 0.6] for i in range(1, 46)}
    cinta_mock.datos_resultados_tester = ResultadosDelInstrumentoDelTester(
        valores_crudos_cuarenta_y_cinco_indicadores=vars_demo,
        numero_de_iteracion_actual=1
    )

    # Bucle de Resiliencia del Test
    auditoria_activa = True
    while auditoria_activa:
        # El orquestador llamaría a este método
        avanzar = GestorDeIntervencionHumanaV7.presentar_auditoria_v7(cinta_mock)
        
        if avanzar:
            TM.evento("SISTEMA", "Prueba finalizada. El Auditor ha dado paso a la fase matemática.")
            auditoria_activa = False
        else:
            TM.evento("SISTEMA", "Simulando evolución del enjambre...")
            time.sleep(1)
            # Mejoramos los valores artificialmente para la demo
            for k in cinta_mock.datos_resultados_tester.valores_crudos_cuarenta_y_cinco_indicadores:
                cinta_mock.datos_resultados_tester.valores_crudos_cuarenta_y_cinco_indicadores[k].append(
                    random.uniform(0.6, 0.95)
                )
            cinta_mock.datos_resultados_tester.numero_de_iteracion_actual += 1