#!/bin/bash
# =============================================================================
# PROYECTO: SYMBIOMEMESIS v7.0 - UNIVERSIDAD DEL ROSARIO
# SCRIPT: Orquestador con Reporte de Inicio (v7.9.3)
# AUTOR: Ing. Fredy Alejandro Sarmiento Torres
# =============================================================================

ENTORNO="venvFIS_Rosario"
ORQUESTADOR="fis_orquestador_v7.py"

echo "🏫 Iniciando Ecosistema Symbiomemesis v7.0..."

# 1. Limpieza de Caja Blanca
echo "🧹 Limpiando artefactos de compilación..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# 2. Localización Dinámica de Conda
CONDA_BASE=$(conda info --base 2>/dev/null)
if [ -z "$CONDA_BASE" ]; then
    CONDA_BASE="/home/fredyast/miniconda"
fi
source "$CONDA_BASE/etc/profile.d/conda.sh"

# 3. Lanzar Streamlit en segundo plano
echo "🚀 Lanzando Orquestador Maestro (Streamlit)..."
conda activate $ENTORNO
streamlit run $ORQUESTADOR &
sleep 2

# 4. PASO FINAL: Inyección de comandos de auditoría en la nueva Shell
echo "🕵️ Terminal de Control activa para el Auditor Fredy."
echo "🔄 Entrando en entorno $ENTORNO..."

# Definimos los comandos iniciales que queremos ver al entrar
COMANDOS_INICIO="
source $CONDA_BASE/etc/profile.d/conda.sh; 
conda activate $ENTORNO; 
echo '--------------------------------------------------';
echo '📊 ESTADO DEL REPOSITORIO (GIT):';
git status -s; 
echo '--------------------------------------------------';
echo '📂 ARCHIVOS DE DATOS RECIENTES:';
ls -lh data/ | head -n 5;
echo '--------------------------------------------------';
"

exec bash --init-file <(echo "$COMANDOS_INICIO")