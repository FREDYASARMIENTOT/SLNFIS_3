"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.1 - UNIVERSIDAD DEL ROSARIO
MODULO: Agente Chatbot Forense Razonador (RAG + CoT + Telemetría v8.1)
UBICACIÓN: /FIS_VERSION8/
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Asistente experto en lenguaje natural con soporte para telemetría forense.
    UPGRADE: Motor actualizado a gemini-2.5-flash (Alta velocidad, bajo costo).
=============================================================================
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Tuple

try:
    import streamlit as st
except ImportError:
    pass

class AgenteChatbotV8:
    """
    Cerebro Narrativo del Enjambre.
    Integra razonamiento multivariado con acceso a la memoria forense local y vectorial.
    """
    
    @staticmethod
    def renderizar_interfaz(cinta):
        st.subheader("🤖 Consultor Forense Symbiomemesis")
        chat_placeholder = st.container(height=450, border=True)
        
        for chat in cinta.bitacora_conversacional:
            with chat_placeholder.chat_message(chat["role"]):
                st.markdown(chat["content"])
                if "contexto" in chat and chat["contexto"]:
                    with st.expander("Ver Evidencia Vectorial (Pinecone)"):
                        st.json(chat["contexto"])

        if prompt := st.chat_input("Consulte el estado del arsenal o la utilidad..."):
            cinta.bitacora_conversacional.append({"role": "user", "content": prompt})
            with chat_placeholder.chat_message("user"):
                st.markdown(prompt)

            with chat_placeholder.chat_message("assistant"):
                with st.spinner("Consultando Cinta y Base Vectorial con Gemini 2.5..."):
                    respuesta_final, contexto_forense = AgenteChatbotV8.procesar_razonamiento(cinta, prompt=prompt)
                    st.markdown(respuesta_final)
                    
                    cinta.bitacora_conversacional.append({
                        "role": "assistant", 
                        "content": respuesta_final,
                        "contexto": contexto_forense
                    })

    @staticmethod
    def procesar_razonamiento(cinta, **kwargs) -> Tuple[str, List]:
        prompt = kwargs.get('prompt', "Por favor, analiza el estado actual del sistema.")
        monitor = kwargs.get('monitor_forense')
        
        # LECTURA DINÁMICA DEL MODELO 2.5 DESDE EL .ENV
        modelo_activo = os.getenv("MODEL_NAME", "gemini-2.5-flash") 
        
        if not cinta.bitacora_forense and hasattr(cinta, 'guardar_estado_v8'):
             ruta_ckpt = "LOGS_v8/cinta_v8_checkpoint.json"
             if os.path.exists(ruta_ckpt):
                 try:
                     with open(ruta_ckpt, "r", encoding="utf-8") as f:
                         data = json.load(f)
                         cinta.datos_matriz_auditoria = data.get("datos_matriz_auditoria", {})
                         cinta.datos_reporte_financiero = data.get("datos_reporte_financiero", {})
                 except: pass

        costo_abc = 0.0
        if hasattr(cinta.datos_reporte_financiero, 'costo_total_calculado'):
            costo_abc = cinta.datos_reporte_financiero.costo_total_calculado
        elif isinstance(cinta.datos_reporte_financiero, dict):
            costo_abc = cinta.datos_reporte_financiero.get('costo_total_calculado', 0.0)
            
        u_val = cinta.datos_matriz_auditoria.get('valor_u', 'No calculada')
        diag = cinta.datos_matriz_auditoria.get('diagnostico_final', 'No disponible')
        etapa = cinta.etapa_actual
        
        contexto_vectorial = AgenteChatbotV8._consultar_pinecone_v8(prompt)
        
        instruccion_forense = f"""
        Eres el Consultor Forense de Symbiomemesis v8.1. 
        Analiza el estado actual para el Ing. Fredy Alejandro Sarmiento Torres:
        
        DATOS DE LA CINTA:
        - ETAPA ACTUAL: {etapa}
        - UTILIDAD U (BIENESTAR): {u_val}
        - DIAGNÓSTICO PREVIO: {diag}
        - COSTO TOTAL REGISTRADO: ${costo_abc:,.2f}
        - EVIDENCIAS VECTORIALES: {json.dumps(contexto_vectorial)}
        
        INSTRUCCIÓN: Responde con rigor científico y tono doctoral. Si los valores de utilidad son 0 o nan, 
        indica que el sistema requiere la ejecución de los agentes Tester y ABC.
        """
        
        try:
            from google import genai
            client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
            
            # INVOCACIÓN A GEMINI 2.5 FLASH
            response = client.models.generate_content(
                model=modelo_activo,
                contents=f"{instruccion_forense}\n\nPREGUNTA DEL AUDITOR: {prompt}"
            )
            
            respuesta = response.text
            
            if monitor:
                monitor.cot_text = f"Razonamiento RAG ({modelo_activo}) completado exitosamente."
                
            return respuesta, contexto_vectorial
            
        except Exception as e:
            return f"⚠️ Error en motor Gemini: {str(e)}", []

    @staticmethod
    def _consultar_pinecone_v8(query: str) -> List[Dict]:
        try:
            from google import genai
            from pinecone import Pinecone
            
            client_g = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
            pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
            idx = pc.Index(os.getenv("PINECONE_INDEX", "symbiomemesis-v7-index"))
            
            res_emb = client_g.models.embed_content(model="text-embedding-004", contents=query)
            
            busqueda = idx.query(
                vector=res_emb.embeddings[0].values, 
                top_k=2, 
                include_metadata=True, 
                namespace="auditoria-v8-forense"
            )
            return [m['metadata'] for m in busqueda['matches']]
        except:
            return []