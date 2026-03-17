"""
=============================================================================
PROYECTO: SYMBIOMEMESIS v7.0 - UNIVERSIDAD DEL ROSARIO
MODULO: Motor de Renderizado PDF — Auditoría Integral de Caja Blanca
AUTOR: Ing. Fredy Alejandro Sarmiento Torres
DESCRIPCIÓN: 
    Renderizado de alta fidelidad. Soporta trazabilidad estigmérgica, 
    fórmulas matemáticas de Utilidad U y Libro Mayor Forense.
    Blindado contra errores de tipado y fallos de concatenación.
=============================================================================
"""

import os
import numpy as np
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

# --- PALETA INSTITUCIONAL UR ---
UR_VINO         = HexColor("#6B0F2B")
UR_DORADO       = HexColor("#C5A059")
UR_GRIS_OSCURO  = HexColor("#1E1E1E")
UR_GRIS_SUAVE   = HexColor("#F4F2F0")
UR_BLANCO       = colors.white

# =============================================================================
# 🎨 COMPONENTES ESTÉTICOS
# =============================================================================

class LineaDivisoria(Flowable):
    def __init__(self, width, color=UR_VINO):
        super().__init__()
        self.width = width
        self.color = color
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(0.5)
        self.canv.line(0, 0, self.width, 0)

def estilos_ur():
    styles = getSampleStyleSheet()
    custom = {
        "title": ParagraphStyle("T", parent=styles["Heading1"], fontSize=18, textColor=UR_VINO, alignment=TA_CENTER, spaceAfter=20),
        "h2": ParagraphStyle("H2", fontSize=11, fontName="Helvetica-Bold", textColor=UR_VINO, spaceBefore=12, spaceAfter=8),
        "body": ParagraphStyle("B", fontSize=8, leading=10, textColor=UR_GRIS_OSCURO, alignment=TA_JUSTIFY),
        "chat_u": ParagraphStyle("CU", fontSize=7.5, leftIndent=5, textColor=colors.navy, spaceBefore=4),
        "chat_ai": ParagraphStyle("CAI", fontSize=7.5, leftIndent=15, textColor=UR_VINO, fontName="Helvetica-Oblique", spaceBefore=4),
        "formula": ParagraphStyle("F", fontName="Times-BoldItalic", fontSize=13, alignment=TA_CENTER, textColor=UR_VINO, spaceBefore=15, spaceAfter=15),
        "mono": ParagraphStyle("M", fontName="Courier", fontSize=7, leading=9, textColor=colors.black, backColor=UR_GRIS_SUAVE)
    }
    return custom

# =============================================================================
# 🚀 MOTOR DE RENDERIZADO (GENERADOR V7.5)
# =============================================================================

class GeneradorReporteV7:
    
    @staticmethod
    def _añadir_pie_pagina(canvas, doc):
        """Añade numeración de página y marca de agua institucional."""
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        page_num = f"Página {doc.page}"
        canvas.drawRightString(200*mm, 10*mm, page_num)
        canvas.drawString(15*mm, 10*mm, "Symbiomemesis v7.0 - Universidad del Rosario")
        canvas.restoreState()

    @staticmethod
    def generar_pdf(cinta):
        os.makedirs("LOGS", exist_ok=True)
        # Sincronización de ruta segura (Solución al TypeError)
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_proy = getattr(cinta, 'identificador_proyecto', 'PROYECTO_ICT').replace(" ", "_")
        path = f"LOGS/INFORME_{nombre_proy}_{ts}.pdf"
        
        doc = SimpleDocTemplate(
            path, 
            pagesize=A4, 
            leftMargin=18*mm, rightMargin=18*mm, 
            topMargin=25*mm, bottomMargin=20*mm
        )
        
        est = estilos_ur()
        story = []

        # --- 1. PORTADA Y METADATOS ---
        logo_path = "ARCHIVOS/logo ur.webp"
        if os.path.exists(logo_path):
            try:
                story.append(Image(logo_path, width=50*mm, height=20*mm))
            except: pass
        
        story.append(Spacer(1, 5*mm))
        story.append(Paragraph("EXPEDIENTE DE AUDITORÍA DE CAJA BLANCA", est["title"]))
        story.append(LineaDivisoria(175*mm))
        story.append(Spacer(1, 10*mm))

        # Tabla de Metadatos blindada con getattr
        id_proy = getattr(cinta, 'identificador_proyecto', 'Symbiomemesis v7.0')
        etapa = getattr(cinta, 'etapa_actual', 'FINALIZACIÓN')
        
        meta = [
            [Paragraph("<b>AUDITOR LÍDER:</b>", est["body"]), "Ing. Fredy Alejandro Sarmiento Torres"],
            [Paragraph("<b>PROYECTO ID:</b>", est["body"]), id_proy],
            [Paragraph("<b>ESTADO CONVERGENCIA:</b>", est["body"]), etapa],
            [Paragraph("<b>FECHA EMISIÓN:</b>", est["body"]), datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        ]
        t_meta = Table(meta, colWidths=[50*mm, 125*mm])
        t_meta.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, UR_DORADO),
            ('BACKGROUND', (0,0), (0,-1), UR_GRIS_SUAVE),
            ('PADDING', (0,0), (-1,-1), 6),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
        ]))
        story.append(t_meta)
        story.append(Spacer(1, 15*mm))

        # --- 2. TRAZABILIDAD HITL ---
        story.append(Paragraph("01. TRAZABILIDAD DEL DIÁLOGO (AUDITOR ↔ ENJAMBRE)", est["h2"]))
        conversacion = getattr(cinta, 'bitacora_conversacional', [])
        if conversacion:
            for chat in conversacion:
                story.append(Paragraph(f"👤 <b>USER:</b> {chat.user_prompt}", est["chat_u"]))
                story.append(Paragraph(f"🤖 <b>AI:</b> {chat.ai_response}", est["chat_ai"]))
        else:
            story.append(Paragraph("<i>No se registran interacciones críticas en esta sesión.</i>", est["body"]))

        # --- 3. LIQUIDACIÓN FINANCIERA ABC ---
        finanzas = getattr(cinta, 'datos_reporte_financiero', None)
        if finanzas:
            story.append(Paragraph("02. LIQUIDACIÓN FINANCIERA ABC (ACTIVITY BASED COSTING)", est["h2"]))
            desglose = getattr(finanzas, 'desglose_de_costos_por_categoria', {})
            data_fin = [["Categoría de Costeo", "Inversión Auditada (COP)"]]
            for cat, val in desglose.items():
                data_fin.append([cat.replace("_", " ").title(), f"$ {val:,.2f}"])
            
            total = getattr(finanzas, 'costo_total_calculado', 0.0)
            data_fin.append([Paragraph("<b>TOTAL LIQUIDADO</b>", est["body"]), f"<b>$ {total:,.2f}</b>"])
            
            t_fin = Table(data_fin, colWidths=[105*mm, 70*mm])
            t_fin.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), UR_VINO),
                ('TEXTCOLOR', (0,0), (-1,0), UR_BLANCO),
                ('ALIGN', (1,1), (1,-1), 'RIGHT'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('FONTSIZE', (0,0), (-1,-1), 9)
            ]))
            story.append(t_fin)

        # --- 4. MALLA ESTOCÁSTICA (BLINDAJE DE DICCIONARIO) ---
        tester = getattr(cinta, 'datos_resultados_tester', None)
        if tester:
            story.append(PageBreak())
            story.append(Paragraph("03. VALORACIÓN DE INDICADORES (MALLA DE 45 VARIABLES)", est["h2"]))
            indicadores = getattr(tester, 'valores_crudos_cuarenta_y_cinco_indicadores', {})
            
            if isinstance(indicadores, dict) and len(indicadores) > 0:
                try:
                    primer_val = next(iter(indicadores.values()))
                    n_med = len(primer_val) if isinstance(primer_val, list) else 1
                    header = ["Indicador"] + [f"M{i+1}" for i in range(n_med)] + ["Promedio"]
                    data_med = [header]
                    
                    for var, vals in list(indicadores.items())[:30]: # Limitado a 30 por página
                        v_list = vals if isinstance(vals, list) else [vals]
                        row = [var[:42], *[f"{v:.3f}" for v in v_list], f"{np.mean(v_list):.4f}"]
                        data_med.append(row)

                    t_ind = Table(data_med, colWidths=[70*mm] + [15*mm]*n_med + [20*mm], repeatRows=1)
                    t_ind.setStyle(TableStyle([
                        ('FONTSIZE', (0,0), (-1,-1), 6.5),
                        ('GRID', (0,0), (-1,-1), 0.3, colors.grey),
                        ('BACKGROUND', (0,0), (-1,0), UR_DORADO),
                        ('ROWBACKGROUNDS', (0,1), (-1,-1), [UR_BLANCO, UR_GRIS_SUAVE])
                    ]))
                    story.append(t_ind)
                except Exception as e:
                    story.append(Paragraph(f"<i>Fallo en visualización de malla: {str(e)}</i>", est["body"]))
            else:
                story.append(Paragraph("<i>Datos estocásticos insuficientes para renderizado.</i>", est["body"]))

        # --- 5. RESOLUCIÓN MATEMÁTICA U ---
        matriz = getattr(cinta, 'datos_matriz_auditoria', None)
        if matriz:
            story.append(Paragraph("04. RESOLUCIÓN MATEMÁTICA DE UTILIDAD SIMBIÓTICA (U)", est["h2"]))
            # Fórmula Doctoral
            story.append(Paragraph("U = Σ · [ ⊥ / (1 + Fricción) ] · (Machine_Learning + Costo_Fin)", est["formula"]))
            
            obs = getattr(matriz, 'observaciones_cualitativas_del_auditor', 'Sin dictamen.')
            story.append(Paragraph(f"<b>Dictamen Forense:</b> {obs}", est["body"]))
            
            pasos = getattr(matriz, 'desarrollo_matematico_paso_a_paso', [])
            for paso in pasos:
                story.append(Paragraph(f"▶ {paso}", est["mono"]))

        # --- 6. LIBRO MAYOR (TRACE) ---
        story.append(PageBreak())
        story.append(Paragraph("05. LIBRO MAYOR FORENSE (TRAZABILIDAD VECTORIAL)", est["h2"]))
        
        bitacora = getattr(cinta, 'bitacora_forense', [])
        data_led = [["Marca de Tiempo", "Agente", "Acción Ejecutada", "Vector ID"]]
        
        # Muestra los últimos 25 registros para auditoría
        for reg in bitacora[-25:]:
            ts = getattr(reg, 'marca_de_tiempo', 'N/A')
            data_led.append([
                ts, 
                getattr(reg, 'emisor', 'N/A'), 
                Paragraph(getattr(reg, 'mensaje_accion', 'N/A')[:90], est["body"]), 
                getattr(reg, 'vector_id', 'N/A')[:12]
            ])
            
        t_led = Table(data_led, colWidths=[35*mm, 30*mm, 75*mm, 35*mm])
        t_led.setStyle(TableStyle([
            ('FONTSIZE', (0,0), (-1,-1), 6.5),
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('BACKGROUND', (0,0), (-1,0), UR_GRIS_OSCURO),
            ('TEXTCOLOR', (0,0), (-1,0), UR_BLANCO),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
        ]))
        story.append(t_led)

        # GENERACIÓN FINAL CON NUMERACIÓN
        try:
            doc.build(story, onFirstPage=GeneradorReporteV7._añadir_pie_pagina, onLaterPages=GeneradorReporteV7._añadir_pie_pagina)
            return path
        except Exception as e:
            print(f"Error crítico en construcción de PDF: {e}")
            return None