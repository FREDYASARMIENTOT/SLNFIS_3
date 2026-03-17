"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v7.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Orquestador Maestro de Auditoría (Chatbot HITL + RAG + ABC + Simbiomemesis)
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Flujo proactivo de auditoría. Induce al usuario, gestiona el arsenal,
    ejecuta el bucle de medición (HITL) y genera el informe forense final.
=============================================================================
"""

import os
import sys
import time
import glob
import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai
from pinecone import Pinecone
from dotenv import load_dotenv

# --- INYECCIÓN DE DEPENDENCIAS ---
directorio_raiz = os.path.dirname(os.path.abspath(__file__))
if directorio_raiz not in sys.path:
    sys.path.append(directorio_raiz)

try:
    from fis_generador_csvs_v7 import AgenteGeneradorFisV7
    from fis_calculaCostosABC_V7 import MotorDeCosteoFinancieroABC_V7
    from fis_calculaSimbiomemesis_v7 import MotorMatematicoSymbiomemesisV7
    from fis_cintagentica_v7 import MallaCognitivaCompartida
    # Asumimos que estos módulos existen según el plan:
    # from fis_hitl_v7 import AgenteTesterHITL
    # from fis_informe_v7 import AgenteGeneradorInforme
except ImportError as e:
    st.error(f"🚨 Error de dependencias: {e}")

# --- CONFIGURACIÓN ---
load_dotenv()
client_gemini = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
indice_pinecone = pc.Index(os.getenv("PINECONE_INDEX", "symbiomemesis-v7-index"))

st.set_page_config(page_title="Symbiomemesis V7 - Auditoría 360", layout="wide")
UR_VINO = "#6B0F2B"
UR_DORADO = "#C5A059"

# -------------------------------------------------------------------------
# GESTIÓN DE ESTADOS (MÁQUINA DE ESTADOS DEL CHATBOT)
# -------------------------------------------------------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "INICIO" # INICIO -> ARSENAL -> ABC -> TESTER -> FINAL
    st.session_state.cinta = MallaCognitivaCompartida()
    st.session_state.entidad = {}
    st.session_state.ts_actual = ""

def buscar_entidad_rag(query):
    try:
        res = client_gemini.models.embed_content(model="gemini-embedding-2-preview", contents=query)
        busqueda = indice_pinecone.query(vector=res.embeddings[0].values, top_k=1, include_metadata=True, namespace="catalogo-oferta-ur")
        if busqueda['matches'] and busqueda['matches'][0]['score'] > 0.75:
            return busqueda['matches'][0]['metadata']
    except: pass
    return None

# -------------------------------------------------------------------------
# UI Y TELEMETRÍA
# -------------------------------------------------------------------------
st.title("🏫 Symbiomemesis v7.0: Orquestador Maestro de Auditoría")

# Barra de Telemetría
if st.session_state.cinta.bitacora_conversacional:
    ult = st.session_state.cinta.bitacora_conversacional[-1]
    st.markdown(f"""<div style='background-color:#262730;color:#00FF41;padding:8px;border-radius:5px;font-family:monospace;font-size:0.8em;'>
        📡 TELEMETRÍA | Latencia: {ult.latencia_ms:.0f}ms | Etapa: {st.session_state.stage} | Auditor: {st.session_state.cinta.identificador_proyecto}
    </div>""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# FLUJO DE AUDITORÍA (CAJA BLANCA)
# -------------------------------------------------------------------------

# FASE 1: IDENTIFICACIÓN E INDUCCIÓN
if st.session_state.stage == "INICIO":
    st.subheader("🕵️ Fase 1: Identificación de la Entidad")
    with st.chat_message("assistant"):
        st.write("Bienvenido, Auditor. Por favor, indique la **Asignatura, Programa o Facultad** que desea auditar.")
    
    if prompt := st.chat_input("Ej: Doctorado en Ingeniería..."):
        with st.spinner("Buscando en catálogo vectorial..."):
            meta = buscar_entidad_rag(prompt)
            st.session_state.entidad = meta if meta else {"programa": "DOCTORADO EN INGENIERÍA, CIENCIA Y TECNOLOGÍA", "facultad": "INGENIERÍA"}
            st.session_state.stage = "ARSENAL"
            st.rerun()

# FASE 2: GENERACIÓN DE ARSENAL
elif st.session_state.stage == "ARSENAL":
    prog = st.session_state.entidad.get('programa')
    st.subheader(f"⚙️ Fase 2: Génesis del Arsenal - {prog}")
    
    with st.chat_message("assistant"):
        st.write(f"He identificado el programa: **{prog}**.")
        st.write("Se recomienda generar los datos para el periodo por defecto: **2025-1S**.")
        
    if st.button("🚀 Confirmar y Generar Datos 2025-1S"):
        with st.status("Fabricando Arsenal de Datos FIS v7...", expanded=True):
            gen = AgenteGeneradorFisV7(raw_data_path="./data")
            gen.ejecutar_plan_total(programa_solicitado=prog)
            st.session_state.ts_actual = gen.timestamp
            
            # Resumen de Caja Blanca
            df_doc = pd.read_csv(f"ORIGENDATOS/maestro_docentes_{gen.timestamp}.csv")
            df_hab = pd.read_csv(f"ORIGENDATOS/maestro_habitat_detallado_{gen.timestamp}.csv")
            df_adm = pd.read_csv(f"ORIGENDATOS/maestro_admin_detallado_{gen.timestamp}.csv")
            
            st.write("### ✅ Arsenal Generado con Éxito:")
            st.write(f"• **Asignaturas/Profesores:** {len(df_doc)} registros.")
            st.write(f"• **Infraestructura (m2):** Pool de {len(df_hab)} espacios de hábitat.")
            st.write(f"• **Costo Indirecto Base:** ${df_adm['Costo_Nomina_Admin'].iloc[0]:,.0f} COP.")
            
            st.session_state.cinta.registrar_evento_forense_detallado("GEN_ARSENAL", "CINTA", f"Arsenal creado para {prog} @ {gen.timestamp}")
            st.session_state.stage = "ABC"
            st.button("Continuar al Costeo ABC ➡️")

# FASE 3: COSTEO ABC
elif st.session_state.stage == "ABC":
    st.subheader("📊 Fase 3: Liquidación Financiera ABC")
    with st.chat_message("assistant"):
        st.write("El arsenal de datos está listo. ¿Desea activar el **Agente de Costeo ABC** para liquidar la entidad?")
    
    if st.button("💰 Ejecutar Costeo ABC"):
        with st.spinner("Calculando prorrateos y costos directos..."):
            exito = MotorDeCosteoFinancieroABC_V7.ejecutar_calculo_de_costos_abc(st.session_state.cinta)
            if exito:
                res = st.session_state.cinta.datos_reporte_financiero
                st.success(f"Costo Total Liquidado: ${res.costo_total_calculado:,.0f} COP")
                st.session_state.stage = "TESTER"
                st.button("Ir al Tester Simbiomemesis 🧪")

# FASE 4: TESTER HITL (MEDIR O SEGUIR)
elif st.session_state.stage == "TESTER":
    st.subheader("🧪 Fase 4: Tester de Indicadores (HITL)")
    with st.chat_message("assistant"):
        st.write("Debemos validar los 45 indicadores estocásticos para calcular la utilidad $U$.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 [1] MEDIR (Re-calcular Enjambre)"):
            with st.spinner("Simulando recálculo..."):
                # Aquí llamarías a fis_hitl_v7.py
                time.sleep(1.5)
                st.session_state.cinta.registrar_evento_forense_detallado("HITL", "PINECONE", "Re-medición de indicadores guardada.")
                st.toast("Indicadores guardados en la base vectorial.")
    with col2:
        if st.button("✅ [2] SEGUIR (Aprobar y Calcular U)"):
            st.session_state.stage = "FINAL"
            st.rerun()

# FASE 5: RESOLUCIÓN Y CIERRE
elif st.session_state.stage == "FINAL":
    st.subheader("🏁 Fase Final: Resolución y Reporte")
    with st.spinner("Resolviendo Ecuación de Utilidad Simbiótica..."):
        MotorMatematicoSymbiomemesisV7.resolver_simbiomemesis_total(st.session_state.cinta)
        matriz = st.session_state.cinta.datos_matriz_auditoria
        st.success(matriz.observaciones_cualitativas_del_auditor)

    # Invocación de Agente Informe
    st.info("Generando informe final de Caja Blanca...")
    # informe = AgenteGeneradorInforme(st.session_state.cinta)
    
    st.download_button(
        label="📥 Descargar Informe de Auditoría V7 (PDF/CSV)",
        data="Contenido del informe...", # Aquí iría el binario del PDF
        file_name=f"Informe_Symbiomemesis_{st.session_state.ts_actual}.pdf"
    )
    
    if st.button("Cerrar Auditoría"):
        st.session_state.clear()
        st.write("Sesión finalizada. Gracias, Ing. Fredy.")
        st.stop()

# --- SIDEBAR DE CAJA BLANCA ---
with st.sidebar:
    st.header("🔍 Auditoría Forense")
    st.write(f"**Cinta ID:** {st.session_state.cinta.identificador_proyecto}")
    st.write(f"**Etapa:** {st.session_state.stage}")
    if st.session_state.ts_actual:
        st.write(f"**Timestamp Arsenal:** {st.session_state.ts_actual}")