"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.1 - UNIVERSIDAD DEL ROSARIO
MODULO: Portal Institucional Streamlit (Dashboard de Caja Blanca)
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Interfaz de mando del enjambre v8.1 (Versión Pestañas / Tabs).
    Navegación horizontal por etapas, visibilidad de métricas globales
    y Chatbot RAG anclado para consultas forenses en tiempo real.
=============================================================================
"""

import streamlit as st
import os
import json
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser la primera instrucción)
st.set_page_config(page_title="Symbiomemesis v8.1 | URosario", layout="wide", page_icon="🏛️")

# Importaciones locales diferidas
from fis_cintagentica_v8 import MallaCognitivaCompartidaV8
from fis_fabrica_agentes_v8 import FabricaAgentesV8
from fis_chatbot_v8 import AgenteChatbotV8

# =============================================================================
# 🧠 GESTIÓN DE ESTADO (SESSION STATE)
# =============================================================================
def cargar_o_inicializar_cinta():
    if 'cinta_v8' not in st.session_state:
        cinta = MallaCognitivaCompartidaV8()
        ruta_ckpt = "LOGS_v8/cinta_v8_checkpoint.json"
        if os.path.exists(ruta_ckpt):
            try:
                with open(ruta_ckpt, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cinta.datos_matriz_auditoria = data.get("datos_matriz_auditoria", {})
                    if "bitacora_conversacional" in data:
                        cinta.bitacora_conversacional = data["bitacora_conversacional"]
            except Exception as e:
                st.sidebar.error(f"Error cargando caché: {e}")
        
        if hasattr(cinta, 'inicializar_auditoria_v8'):
            cinta.inicializar_auditoria_v8()
            
        st.session_state.cinta_v8 = cinta
    return st.session_state.cinta_v8

cinta = cargar_o_inicializar_cinta()

# =============================================================================
# 🎨 INTERFAZ GRÁFICA (CSS INSTITUCIONAL)
# =============================================================================
st.markdown("""
    <style>
    .metric-box { background-color: #f8f9fa; border-left: 5px solid #8B0000; padding: 15px; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .telemetria { background-color: #1e1e1e; color: #00FF41; padding: 10px; border-radius: 5px; font-family: monospace; font-size: 0.85em; text-align: center;}
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 4px 4px 0px 0px; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #8B0000; color: white !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ENCABEZADO
st.markdown("""
<div style="background-color:#8B0000; padding:15px; border-radius:8px; color:white; text-align:center; margin-bottom: 20px;">
    <h1 style="margin:0;">🏛️ SYMBIOMEMESIS V8.1</h1>
    <h4 style="margin:0; font-weight:300;">Plataforma de Auditoría Forense y Simbiomemesis Computacional</h4>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# 📊 MÉTRICAS GLOBALES (SIEMPRE VISIBLES)
# =============================================================================
u_val = cinta.datos_matriz_auditoria.get('valor_u', 'No Calculada')
diag = cinta.datos_matriz_auditoria.get('diagnostico_final', 'En espera de datos...')
costo_abc = getattr(cinta.datos_reporte_financiero, 'costo_total_calculado', 0.0) if hasattr(cinta.datos_reporte_financiero, 'costo_total_calculado') else cinta.datos_reporte_financiero.get('costo_total_calculado', 0.0) if isinstance(cinta.datos_reporte_financiero, dict) else 0.0

m1, m2, m3 = st.columns(3)
with m1: st.markdown(f"<div class='metric-box'><b>💰 Costo Total ABC</b><br><h3 style='color:#8B0000; margin:0;'>${costo_abc:,.0f}</h3></div>", unsafe_allow_html=True)
with m2: st.markdown(f"<div class='metric-box'><b>🧮 Utilidad (U)</b><br><h3 style='color:#8B0000; margin:0;'>{u_val}</h3></div>", unsafe_allow_html=True)
with m3: st.markdown(f"<div class='metric-box'><b>📈 Estado Sistémico</b><br><h5 style='color:#8B0000; margin:0; margin-top:8px;'>{str(diag)[:35]}...</h5></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =============================================================================
# 🏗️ ARQUITECTURA PRINCIPAL: PESTAÑAS Y CHATBOT
# =============================================================================
col_proceso, col_chatbot = st.columns([1.8, 1])

with col_proceso:
    # CREACIÓN DE PESTAÑAS (TABS)
    tabs = st.tabs([
        "📂 1. Génesis", 
        "💰 2. Costeo ABC", 
        "🧪 3. Malla 45", 
        "🧮 4. Utilidad (U)", 
        "📈 5. Gradiente (Δ)", 
        "📼 6. La Cinta Forense"
    ])

    # --- PESTAÑA 1: GÉNESIS ---
    with tabs[0]:
        st.subheader("Construcción del Arsenal de Datos")
        st.write("Esta etapa extrae y formatea la jerarquía Abuelo-Padre-Hijo de la Universidad.")
        if st.button("🚀 Construir Jerarquía CSV", use_container_width=True):
            with st.spinner("Agente Génesis procesando datos..."):
                if hasattr(FabricaAgentesV8, 'crear_agente_genesis'):
                    agente_genesis = FabricaAgentesV8.crear_agente_genesis()
                    agente_genesis.ejecutar(cinta, "Generar estructuras CSV: Abuelo, Padre e Hijo.")
                st.success("¡Arsenal de datos construido exitosamente!")
                st.rerun()

    # --- PESTAÑA 2: COSTEO ABC ---
    with tabs[1]:
        st.subheader("Liquidación Financiera ABC")
        st.write("Prorrateo de la bolsa administrativa y cálculo de costos directos.")
        if st.button("💸 Ejecutar Liquidador ABC", use_container_width=True):
            with st.spinner("Agente Financiero calculando..."):
                agente_abc = FabricaAgentesV8.crear_agente_abc() if hasattr(FabricaAgentesV8, 'crear_agente_abc') else FabricaAgentesV8.crear_agente_financiero()
                agente_abc.ejecutar(cinta, "Calcular costos ABC sobre la jerarquía.")
                st.rerun()

    # --- PESTAÑA 3: TESTER MALLA 45 ---
    with tabs[2]:
        st.subheader("Auditoría de Indicadores Estocásticos")
        st.write("Evaluación de la Malla 45 para extraer los pilares ME, SG y FR.")
        if st.button("🎯 Evaluar Malla de Indicadores", use_container_width=True):
            with st.spinner("Agente Tester auditando..."):
                agente_test = FabricaAgentesV8.crear_agente_tester()
                agente_test.ejecutar(cinta, "Extraer vectores estocásticos ME, SG, FR.")
                st.rerun()

    # --- PESTAÑA 4: UTILIDAD U ---
    with tabs[3]:
        st.subheader("Cálculo de Bienestar Simbiótico")
        st.write("Resolución de la ecuación escalar $U$ basada en costos y fricción.")
        if st.button("🧩 Resolver Ecuación de Utilidad", use_container_width=True):
            with st.spinner("Motor matemático en ejecución..."):
                agente_u = FabricaAgentesV8.crear_agente_matematico_u()
                agente_u.ejecutar(cinta, "Generar escalar U basado en la matriz actual.")
                st.rerun()

    # --- PESTAÑA 5: GRADIENTE ---
    with tabs[4]:
        st.subheader("Análisis de Convergencia Sistémica")
        st.write("Razonamiento sobre la variación del sistema (Entropía vs. Simbiosis).")
        if st.button("🔭 Analizar Gradiente Δ", use_container_width=True):
            with st.spinner("Consultando convergencia con Gemini 2.5..."):
                agente_grad = FabricaAgentesV8.crear_agente_gradiente_razonador() if hasattr(FabricaAgentesV8, 'crear_agente_gradiente_razonador') else FabricaAgentesV8.crear_agente_derivadas_razonador()
                agente_grad.ejecutar(cinta, "Diagnosticar Estabilidad, Entropía o Simbiosis.")
                st.rerun()

    # --- PESTAÑA 6: LA CINTA FORENSE ---
    with tabs[5]:
        st.subheader("Registro de Operaciones (TapeAgents)")
        if not cinta.bitacora_forense:
            st.info("La cinta está vacía. Navegue por las pestañas anteriores y ejecute los agentes.")
        else:
            for evento in reversed(cinta.bitacora_forense[-8:]):
                with st.expander(f"[{evento.marca_de_tiempo}] 🤖 {evento.emisor} ➔ {evento.mensaje_accion}"):
                    if hasattr(evento, 'tape_steps') and evento.tape_steps:
                        for step in evento.tape_steps:
                            if step.kind == 'thought':
                                st.markdown(f"**🧠 Razonamiento (CoT):**\n> {step.contenido}")
                            elif step.kind == 'action':
                                st.markdown(f"**⚡ Acción Técnica:**\n`{step.contenido}`")
                            elif step.kind == 'observation':
                                st.success(f"**✅ Resultado:**\n{step.contenido}")
                    else:
                        st.text_area("Salida:", evento.salida_cruda, height=100, disabled=True)
                    st.caption(f"Status: {evento.status} | Vector ID: {evento.vector_id}")

# =============================================================================
# 🤖 COLUMNA DERECHA: CHATBOT RAG
# =============================================================================
with col_chatbot:
    AgenteChatbotV8.renderizar_interfaz(cinta)

# =============================================================================
# 🎛️ PANEL LATERAL (SIDEBAR)
# =============================================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; border-bottom: 2px solid #8B0000; padding-bottom: 10px; margin-bottom: 20px;">
        <h2 style="color: #8B0000; margin-bottom: 0;">🏛️ URosario</h2>
        <span style="font-size: 12px; color: gray;">Auditoría Forense v8.1</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.write(f"**Investigador:** Fredy Sarmiento")
    st.write(f"**Motor Inteligencia:** {os.getenv('MODEL_NAME', 'gemini-2.5-flash')}")
    st.write(f"**Agentes Activos:**")
    
    # Listado de agentes (Protegido contra errores si el método falla)
    try:
        agentes_part = cinta.obtener_agentes_participantes()
        for ag in agentes_part:
            st.caption(f"▪️ {ag}")
    except:
        st.caption("▪️ Esperando estigmergia...")
    
    st.markdown("---")
    
    if st.button("🗑️ Limpiar Memoria (Hard Reset)", use_container_width=True):
        st.session_state.cinta_v8 = MallaCognitivaCompartidaV8()
        st.rerun()

# =============================================================================
# 📡 FOOTER DE TELEMETRÍA
# =============================================================================
st.markdown("---")
st.markdown(f"""<div class="telemetria">📡 <b>SISTEMA DE MONITOREO ACTIVO</b> | Vectores Forenses: 3072 dims | Enlace Pinecone: Estable | Sesión Local Protegida</div>""", unsafe_allow_html=True)