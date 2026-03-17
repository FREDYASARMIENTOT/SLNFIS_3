"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v8.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Motor de Renderizado PDF — Auditoría Integral de Caja Blanca (v8.0)
UBICACIÓN: /FIS_VERSION8/
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Generador de informes de alta fidelidad. Consolida:
    1. Selección Jerárquica (Facultad/Programa/Asignatura).
    2. Bitácora de Telemetría v8 (Tokens, Costos, CoT).
    3. Malla de 45 Indicadores y 15 Variables de Utilidad.
    4. Resolución de Derivadas y Gradientes Simbiomemésicos.
=============================================================================
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable, Image
)
from reportlab.lib.colors import HexColor

# --- IMPORTACIONES DE TELEMETRÍA V8 ---
from fis_telemetria_v8 import TelemetriaMaestraV8 as TM

# --- PALETA INSTITUCIONAL UR V8 ---
UR_VINO         = HexColor("#6B0F2B")
UR_DORADO       = HexColor("#C5A059")
UR_GRIS_OSCURO  = HexColor("#1E1E1E")
UR_GRIS_SUAVE   = HexColor("#F4F2F0")
UR_BLANCO       = colors.white

# =============================================================================
# 🎨 ESTILOS Y COMPONENTES VISUALES
# =============================================================================

class LineaForense(Flowable):
    def __init__(self, width, color=UR_VINO, thickness=1):
        super().__init__()
        self.width = width
        self.color = color
        self.thickness = thickness
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)

def obtener_estilos_v8():
    styles = getSampleStyleSheet()
    return {
        "titulo": ParagraphStyle("T", parent=styles["Heading1"], fontSize=22, textColor=UR_VINO, alignment=TA_CENTER, spaceAfter=30),
        "subtitulo": ParagraphStyle("ST", fontSize=14, textColor=UR_DORADO, alignment=TA_CENTER, spaceAfter=20),
        "h2": ParagraphStyle("H2", fontSize=12, fontName="Helvetica-Bold", textColor=UR_VINO, spaceBefore=15, spaceAfter=10, leftIndent=0),
        "body": ParagraphStyle("B", fontSize=9, leading=11, textColor=UR_GRIS_OSCURO, alignment=TA_JUSTIFY),
        "metadato": ParagraphStyle("M", fontSize=8, fontName="Helvetica-Bold", textColor=colors.grey),
        "cot": ParagraphStyle("COT", fontSize=8, fontName="Helvetica-Oblique", textColor=colors.darkblue, leftIndent=10, spaceBefore=5),
        "formula": ParagraphStyle("F", fontName="Times-BoldItalic", fontSize=14, alignment=TA_CENTER, textColor=UR_VINO, spaceBefore=20, spaceAfter=20, backColor=UR_GRIS_SUAVE),
        "mono": ParagraphStyle("MONO", fontName="Courier", fontSize=7, leading=9, textColor=colors.black)
    }

# =============================================================================
# 🚀 GENERADOR DE INFORME DOCTORAL V8
# =============================================================================

class GeneradorReporteV8:
    
    @staticmethod
    def _pie_pagina_v8(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica-Oblique', 8)
        canvas.setFillColor(colors.grey)
        canvas.drawRightString(200*mm, 10*mm, f"Expediente Symbiomemesis v8.0 | Página {doc.page}")
        canvas.drawString(15*mm, 10*mm, "Universidad del Rosario - Escuela de Ingeniería, Ciencia y Tecnología")
        canvas.restoreState()

    @staticmethod
    def generar_pdf_auditoria(cinta):
        """Genera el reporte final con visibilidad total del proceso."""
        os.makedirs("LOGS_v8", exist_ok=True)
        ts = datetime.now().strftime('%Y%m%d_%H%M')
        nombre_proy = getattr(cinta, 'identificador_proyecto', 'UR_AUDIT').replace(" ", "_")
        path_pdf = f"LOGS_v8/INFORME_DOCTORAL_{nombre_proy}_{ts}.pdf"
        
        doc = SimpleDocTemplate(path_pdf, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=25*mm, bottomMargin=25*mm)
        est = obtener_estilos_v8()
        story = []

        # --- 1. PORTADA INSTITUCIONAL ---
        logo = "ARCHIVOS/logo ur.webp"
        if os.path.exists(logo): story.append(Image(logo, width=60*mm, height=25*mm))
        
        story.append(Spacer(1, 20*mm))
        story.append(Paragraph("AUDITORÍA DE CAJA BLANCA SYMBIOMEMESIS", est["titulo"]))
        story.append(Paragraph(f"PROYECTO: {getattr(cinta, 'identificador_proyecto', 'N/A')}", est["subtitulo"]))
        story.append(LineaForense(170*mm, UR_DORADO, 2))
        story.append(Spacer(1, 10*mm))

        # --- 2. ENCABEZADO DE SELECCIÓN JERÁRQUICA ---
        story.append(Paragraph("I. PARÁMETROS DE INDUCCIÓN JERÁRQUICA", est["h2"]))
        # Recuperamos la selección desde la cinta (inyectada por el orquestador)
        seleccion = getattr(cinta, 'seleccion_actual', {})
        data_sel = [
            ["Nivel de Formación", "POSGRADO"],
            ["Facultad / Escuela", seleccion.get('facultad', 'ICT')],
            ["Programa Académico", seleccion.get('programa', 'Doctorado en Ingeniería')],
            ["Asignaturas Auditadas", seleccion.get('asignaturas', 'Todas las seleccionadas')]
        ]
        t_sel = Table(data_sel, colWidths=[60*mm, 110*mm])
        t_sel.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, UR_VINO),
            ('BACKGROUND', (0,0), (0,-1), UR_GRIS_SUAVE),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('PADDING', (0,0), (-1,-1), 8)
        ]))
        story.append(t_sel)
        story.append(Spacer(1, 10*mm))

        # --- 3. BITÁCORA DE TELEMETRÍA Y COSTOS (CAJA BLANCA) ---
        story.append(Paragraph("II. TRAZABILIDAD DE ENJAMBRE (BITÁCORA V8)", est["h2"]))
        story.append(Paragraph("Detalle de ejecución agéntica, razonamiento (CoT) y consumo de recursos.", est["body"]))
        story.append(Spacer(1, 5*mm))

        data_tel = [["Agente", "Modelo", "Costo (USD)", "Razonamiento / Acción"]]
        for reg in TM.bitacora_forense:
            data_tel.append([
                reg.agente.replace("_V8", ""),
                reg.modelo,
                f"${reg.costo_usd:.6f}",
                Paragraph(f"<b>CoT:</b> {reg.cot_text[:150]}...", est["body"])
            ])
        
        t_tel = Table(data_tel, colWidths=[30*mm, 25*mm, 30*mm, 85*mm])
        t_tel.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), UR_VINO),
            ('TEXTCOLOR', (0,0), (-1,0), UR_BLANCO),
            ('GRID', (0,0), (-1,-1), 0.3, colors.grey),
            ('FONTSIZE', (0,0), (-1,-1), 7),
            ('VALIGN', (0,0), (-1,-1), 'TOP')
        ]))
        story.append(t_tel)
        
        # Resumen económico de la sesión
        resumen = TM.obtener_resumen_economico()
        story.append(Spacer(1, 5*mm))
        story.append(Paragraph(f"<b>Gasto Total Inferencia:</b> ${resumen['total_usd']:.4f} USD | <b>Tokens:</b> {resumen['total_tokens']:,}", est["metadato"]))

        # --- 4. MALLA ESTOCÁSTICA Y VARIABLES U ---
        story.append(PageBreak())
        story.append(Paragraph("III. VALORACIÓN DE LA MALLA DE 45 VARIABLES", est["h2"]))
        
        tester = getattr(cinta, 'datos_resultados_tester', None)
        if tester:
            malla = tester.malla_45_completa
            data_malla = [["Indicador", "Valor", "Indicador", "Valor", "Indicador", "Valor"]]
            # Organizar en 3 columnas para ahorrar espacio
            keys = list(malla.keys())
            for i in range(0, 15):
                row = [keys[i], malla[keys[i]], keys[i+15], malla[keys[i+15]], keys[i+30], malla[keys[i+30]]]
                data_malla.append(row)
            
            t_malla = Table(data_malla, colWidths=[40*mm, 15*mm, 40*mm, 15*mm, 40*mm, 15*mm])
            t_malla.setStyle(TableStyle([
                ('FONTSIZE', (0,0), (-1,-1), 6),
                ('GRID', (0,0), (-1,-1), 0.2, colors.lightgrey),
                ('BACKGROUND', (0,0), (-1,0), UR_DORADO),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [UR_BLANCO, UR_GRIS_SUAVE])
            ]))
            story.append(t_malla)

        # --- 5. RESOLUCIÓN MATEMÁTICA Y GRADIENTE ---
        story.append(Spacer(1, 10*mm))
        story.append(Paragraph("IV. RESOLUCIÓN DE UTILIDAD SIMBIÓTICA (U)", est["h2"]))
        
        matriz = getattr(cinta, 'datos_matriz_auditoria', {})
        u_final = matriz.get('valor_u', 0.0)
        
        story.append(Paragraph(f"U = ( Σ Estocástica / (1 + Fricción) ) * Eficiencia_Financiera", est["formula"]))
        story.append(Paragraph(f"VALOR RESULTANTE U: <b>{u_final:.6f}</b>", est["h2"]))
        
        # Desglose matemático paso a paso
        story.append(Paragraph("Desarrollo Matemático de Caja Blanca:", est["body"]))
        for paso in matriz.get('auditoria_forense', {}).get('pasos_detalle', []):
            story.append(Paragraph(f"▶ {paso}", est["mono"]))

        # Análisis de Gradiente
        gradiente = matriz.get('gradiente_v8', {})
        if gradiente:
            story.append(Spacer(1, 5*mm))
            story.append(Paragraph(f"<b>Razón de Cambio (dU/dM):</b> {gradiente.get('razon_de_cambio', 0.0):+.6f}", est["body"]))
            story.append(Paragraph(f"<b>Diagnóstico de Convergencia:</b> {gradiente.get('analisis_convergencia', 'N/A')}", est["body"]))

        # --- 6. CIERRE Y FIRMA ---
        story.append(Spacer(1, 20*mm))
        story.append(LineaForense(50*mm, UR_VINO, 0.5))
        story.append(Paragraph("ING. FREDY ALEJANDRO SARMIENTO TORRES", est["metadato"]))
        story.append(Paragraph("Analista de Información - Universidad del Rosario", est["metadato"]))

        # CONSTRUCCIÓN FINAL
        try:
            doc.build(story, onFirstPage=GeneradorReporteV8._pie_pagina_v8, onLaterPages=GeneradorReporteV8._pie_pagina_v8)
            TM.evento("GENERADOR_PDF", f"Expediente generado exitosamente en: {path_pdf}")
            return path_pdf
        except Exception as e:
            TM.error(f"Error construyendo PDF doctoral: {e}")
            return None

# =============================================================================
# PRUEBA INTEGRAL (MOCK)
# =============================================================================
if __name__ == "__main__":
    class MockCinta:
        def __init__(self):
            self.identificador_proyecto = "TESIS_SYMBIOMEMESIS_V8"
            self.seleccion_actual = {'facultad': 'INGENIERÍA', 'programa': 'DOCTORADO', 'asignaturas': 'Cálculo, IA'}
            self.datos_matriz_auditoria = {'valor_u': 0.8564, 'auditoria_forense': {'pasos_detalle': ['Paso 1: Normalización', 'Paso 2: Prorrateo']}}
    
    GeneradorReporteV8.generar_pdf_auditoria(MockCinta())