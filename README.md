# SYMBIOMEMESIS v7.0: Orquestador de Auditoría Forense 🏫🧬
**Investigación de Maestría en Ingeniería, Ciencia y Tecnología** **Autor:** Ing. Fredy Alejandro Sarmiento Torres  
**Institución:** Universidad del Rosario, Bogotá, Colombia

---

## 📑 Resumen del Proyecto
SYMBIOMEMESIS es un ecosistema de **Inteligencia Artificial Agentica** diseñado para realizar auditorías integrales de "Caja Blanca". A diferencia de los sistemas tradicionales de caja negra, esta plataforma permite una trazabilidad total de cada decisión, cálculo financiero y valoración estocástica mediante una **Malla Cognitiva Compartida (La Cinta)**.

El sistema simula un enjambre de agentes especializados que colaboran estigmérgicamente para determinar la **Utilidad Simbiótica ($U$)** de una entidad académica o administrativa.

---

## ⚙️ Arquitectura de Agentes y Fases

El flujo de trabajo se divide en cinco fases críticas, cada una gobernada por un agente especializado:

### 1. Inducción Jerárquica (Gobernanza)
Utiliza un motor de selección multinivel (**Abuelo-Padre-Hijo**) para delimitar el alcance de la auditoría.
* **Abuelo:** Facultad.
* **Padre:** Programa Académico.
* **Hijo:** Asignatura específica.
* *Tecnología:* Streamlit Cascading Selectors.

### 2. Génesis de Arsenal (Agente Generador)
Transforma la materia prima (Oferta Académica 2024) en un **Arsenal de Datos** normalizado.
* Genera maestros de Docentes, Hábitat (m2 e infraestructura) y Software.
* Garantiza la integridad referencial para el costeo posterior.

### 3. Liquidación ABC (Motor Financiero)
Implementa el modelo de **Costeo Basado en Actividades (Activity Based Costing)**.
* Calcula costos directos e indirectos (Bolsa Administrativa).
* Realiza prorrateos automáticos basados en el uso de hábitat y nómina docente.

### 4. Laboratorio Estocástico (Agente Tester)
Ejecuta el bucle de medición de la **Malla de 45 Variables**.
* Evalúa indicadores de impacto, calidad y eficiencia.
* Persiste cada medición ($M_1, M_2, \dots, M_n$) en un espacio vectorial de **3072 dimensiones**.

### 5. Resolución Symbiomemesis (Motor Matemático)
Aplica el cálculo final de la utilidad mediante la resolución de la ecuación maestra:
$$U = \Sigma \cdot \left[ \frac{\perp}{1 + F} \right] \cdot (ME + C_{bi})$$
* Genera un **Dictamen Forense** y el informe final sellado en PDF.

---

## 🤖 Chatbot de Auditoría RAG (Caja Blanca)
El sistema incluye un asistente de consulta proactivo que utiliza **Generative AI (Gemini 2.0 Flash)** y **Pinecone**.
* **Interrogación Estigmérgica:** El auditor puede preguntar por el origen de cualquier dato.
* **Recuperación Vectorial:** El chatbot busca en el "Libro Mayor" de la Cinta los **Vector IDs** relacionados con la consulta para explicar el razonamiento de los agentes.

---

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3.12 (Aislado en entorno `venvFIS_Rosario`).
* **IA Generativa:** Google Gemini API (Modelos `flash` y `embedding-2-preview`).
* **Base de Datos Vectorial:** Pinecone (Namespace: `auditoria-v7`).
* **Gestión de Datos:** Pandas, Pydantic v2 (Validación de Esquemas).
* **Interfaz:** Streamlit (Arquitectura HITL - Human In The Loop).
* **Reportes:** ReportLab (Renderizado de alta fidelidad para Tesis).

---

## 🚀 Instalación y Uso Rápido (Linux/WSL)

1. **Clonar y Preparar:**
   ```bash
   git clone [https://github.com/FREDYASARMIENTOT/SLNFIS_3.git](https://github.com/FREDYASARMIENTOT/SLNFIS_3.git)
   cd SLNFIS_3