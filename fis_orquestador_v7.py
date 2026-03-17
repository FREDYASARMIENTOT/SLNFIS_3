"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v7.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Orquestador Maestro (v7.9 - Visibilidad Total y Chatbot RAG)
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Mantiene todas las etapas visibles mediante contenedores persistentes.
    Integra Chatbot RAG y Malla Cognitiva sin pérdida de jerarquía.
=============================================================================
"""

import os
import streamlit as st
import pandas as pd
from datetime import datetime

# --- INYECCIÓN DE DEPENDENCIAS ---
from fis_telemetria_v7 import TelemetriaMaestraV7 as TM
from fis_cintagentica_v7 import MallaCognitivaCompartida, RegistroInteraccionChatbot
from fis_generador_csvs_v7 import AgenteGeneradorFisV7
from fis_calculaCostosABC_v7 import MotorDeCosteoFinancieroABC_V7
from fis_agenteTester_v7 import AgenteTesterv7
from fis_calculaSimbiomemesis_v7 import MotorMatematicoSymbiomemesisV7
from fis_informe_v7 import GeneradorReporteV7

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Symbiomemesis V7 - Auditoría 360", layout="wide", page_icon="🏫")

# Estilos Institucionales UR
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #6B0F2B; color: white; border-radius: 8px; font-weight: bold; }
    .stButton>button:hover { background-color: #8B1A3A; color: #C5A059; border: 1px solid #C5A059; }
    [data-testid="stSidebar"] { background-color: #1E1E1E; color: white; }
    .telemetria { background-color:#1e1e1e; color:#00FF41; padding:10px; border-radius:5px; font-family:monospace; font-size:0.85em; border: 1px solid #333; }
    .chat-box { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #6B0F2B; height: 300px; overflow-y: auto; }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 🧠 GESTIÓN DE SESIÓN
# =============================================================================
if "cinta" not in st.session_state:
    st.session_state.cinta = MallaCognitivaCompartida()
    st.session_state.cinta.inicializar_auditoria_financiera()
    st.session_state.stage = "INICIO"
    st.session_state.messages = []

cinta = st.session_state.cinta

@st.cache_data
def cargar_maestro_filtros():
    ruta = "data/OFERTA ACADEMICA ASIGNATURAS 2024.xlsx"
    if os.path.exists(ruta):
        return pd.read_excel(ruta, sheet_name="ClasificaAsignaturas2024UR")
    return pd.DataFrame()

df_m = cargar_maestro_filtros()

# =============================================================================
# 🔍 BARRA LATERAL (TELEMETRÍA FORENSE)
# =============================================================================
with st.sidebar:
    logo = "ARCHIVOS/logo ur.webp"
    if os.path.exists(logo): st.image(logo, width=250)
    st.header("🕵️ Auditoría Forense")
    st.metric("Convergencia Actual", st.session_state.stage)
    
    st.divider()
    st.write("**Rastro de Agentes:**")
    for agente in cinta.obtener_agentes_participantes():
        st.caption(f"🔹 {agente}")
    
    if st.button("🗑️ Reset Malla"):
        st.session_state.clear()
        st.rerun()

# =============================================================================
# 🏗️ ARQUITECTURA DE PANTALLA ÚNICA (VISIBILIDAD TOTAL)
# =============================================================================
st.title("🏫 Symbiomemesis v7.0: Orquestador Maestro")
st.caption(f"Investigador: Ing. Fredy Alejandro Sarmiento Torres | Proyecto: {cinta.identificador_proyecto}")

# layout de dos columnas: Izquierda (Proceso) | Derecha (Chatbot)
col_proceso, col_chatbot = st.columns([2, 1])

with col_proceso:
    # --- ETAPA 1: INDUCCIÓN ---
    with st.expander("1️⃣ INDUCCIÓN JERÁRQUICA (Abuelo-Padre-Hijo)", expanded=(st.session_state.stage == "INICIO")):
        if not df_m.empty:
            c1, c2, c3 = st.columns(3)
            with c1:
                f_sel = st.multiselect("Facultad:", sorted(df_m['FACULTAD_ASIGNATURA'].unique()), default=["ESCUELA DE INGENIERÍA, CIENCIA Y TECNOLOGÍA"])
            with c2:
                df_p = df_m[df_m['FACULTAD_ASIGNATURA'].isin(f_sel)]
                p_sel = st.multiselect("Programa:", sorted(df_p['NOMBRE_PROGRAMA'].unique()), default=["DOCTORADO EN INGENIERÍA, CIENCIA Y TECNOLOGÍA"] if not df_p.empty else [])
            with c3:
                asig_sel = st.multiselect("Asignaturas:", sorted(df_p[df_p['NOMBRE_PROGRAMA'].isin(p_sel)]['NOMBRE_ASIGNATURA'].unique()))
            
            if st.button("🚀 Confirmar Selección"):
                st.session_state.stage = "ARSENAL"
                st.rerun()

    # --- ETAPA 2 & 3: ARSENAL Y ABC ---
    with st.expander("2️⃣ & 3️⃣ ARSENAL Y LIQUIDACIÓN ABC", expanded=(st.session_state.stage in ["ARSENAL", "ABC"])):
        col_btn1, col_btn2 = st.columns(2)
        if col_btn1.button("🔨 Generar Arsenal"):
            AgenteGeneradorFisV7().ejecutar_plan_total(cinta, f_sel, p_sel, asig_sel)
            st.session_state.stage = "ABC"
            st.rerun()
        
        if col_btn2.button("💰 Ejecutar Motor ABC"):
            MotorDeCosteoFinancieroABC_V7.ejecutar_calculo_de_costos_abc(cinta)
            st.session_state.stage = "TESTER"
            st.rerun()
        
        if cinta.datos_reporte_financiero:
            st.metric("TOTAL ABC AUDITADO", f"$ {cinta.datos_reporte_financiero.costo_total_calculado:,.2f} COP")

    # --- ETAPA 4: TESTER ---
    with st.expander("4️⃣ VALORACIÓN ESTOCÁSTICA (M+n)", expanded=(st.session_state.stage == "TESTER")):
        if st.button("🔄 REALIZAR MEDICIÓN"):
            AgenteTesterv7.ejecutar_evaluacion_indicadores(cinta)
            st.toast("Medición guardada en Pinecone.")
        
        if st.button("➡️ Finalizar Bucle de Medición"):
            st.session_state.stage = "FINAL"
            st.rerun()

    # --- ETAPA 5: RESOLUCIÓN ---
    with st.expander("5️⃣ RESOLUCIÓN Y CIERRE", expanded=(st.session_state.stage == "FINAL")):
        if st.button("🧮 Calcular Utilidad U + 📄 PDF"):
            MotorMatematicoSymbiomemesisV7.resolver_simbiomemesis_total(cinta)
            ruta_pdf = GeneradorReporteV7.generar_pdf(cinta)
            st.success("Auditoría Finalizada.")
            if os.path.exists(ruta_pdf):
                with open(ruta_pdf, "rb") as f:
                    st.download_button("📥 Descargar Reporte Doctoral", f, file_name=os.path.basename(ruta_pdf))

# =============================================================================
# 🤖 COLUMNA DERECHA: CHATBOT RAG PERSISTENTE
# =============================================================================
with col_chatbot:
    st.header("🤖 Asistente RAG")
    st.write("Interrogue la Malla Cognitiva:")
    
    # Contenedor de mensajes (Caja Blanca)
    chat_container = st.container(height=400)
    for msg in st.session_state.messages:
        chat_container.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("¿Qué agentes han participado?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        chat_container.chat_message("user").write(prompt)
        
        # Respuesta del asistente consultando la Cinta
        agentes = ", ".join(cinta.obtener_agentes_participantes())
        respuesta = f"Auditor Fredy, en la etapa {st.session_state.stage}, han participado: {agentes}. El costo ABC actual es de ${getattr(cinta.datos_reporte_financiero, 'costo_total_calculado', 0):,.2f}."
        
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
        chat_container.chat_message("assistant").write(respuesta)
        
        # Registro en la Cinta
        cinta.bitacora_conversacional.append(RegistroInteraccionChatbot(user_prompt=prompt, ai_response=respuesta, intent="CONSULTA"))

# =============================================================================
# 📡 TELEMETRÍA (SIEMPRE VISIBLE)
# =============================================================================
st.divider()
st.markdown(f"""<div class="telemetria">📡 <b>TELEMETRÍA DE LA CINTA</b> | Etapa: {st.session_state.stage} | Proyecto: {cinta.identificador_proyecto} | Vectores: 3072 dims</div>""", unsafe_allow_html=True)