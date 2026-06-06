import streamlit as st

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Cyber Security Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# =====================================================
# HEADER
# =====================================================

st.title("🛡️ Cyber Security Dashboard")

st.markdown("""
### Centro de Monitoreo y Análisis de Ciberseguridad

Plataforma diseñada para el monitoreo, análisis e identificación de amenazas,
anomalías y comportamientos sospechosos a partir de eventos de seguridad.
""")

st.divider()

# =====================================================
# KPIs DE PRESENTACIÓN
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📡 Monitoreo",
        "24/7"
    )

with col2:
    st.metric(
        "🔍 Análisis",
        "Tiempo Real"
    )

with col3:
    st.metric(
        "🛡️ Detección",
        "Anomalías"
    )

with col4:
    st.metric(
        "⚠️ Evaluación",
        "Riesgos"
    )

st.divider()

# =====================================================
# DESCRIPCIÓN DE MÓDULOS
# =====================================================

st.subheader("📚 Módulos del Dashboard")

col1, col2 = st.columns(2)

with col1:

    st.info("""
    📊 **Resumen Ejecutivo**

    Visualización general de indicadores,
    anomalías y actividad registrada.
    """)

    st.info("""
    🖥️ **Centro de Monitoreo**

    Supervisión de eventos,
    usuarios, IPs y actividades.
    """)

    st.info("""
    🚨 **Análisis de Anomalías**

    Identificación de comportamientos
    sospechosos y eventos anómalos.
    """)

with col2:

    st.info("""
    ⚠️ **Análisis de Riesgo**

    Clasificación y priorización
    de amenazas detectadas.
    """)

    st.info("""
    🔎 **Explorador de Eventos**

    Búsqueda avanzada e investigación
    de eventos específicos.
    """)

    st.info("""
    🕵️ **Threat Intelligence**

    Inteligencia de amenazas,
    correlación y análisis estratégico.
    """)

st.divider()

# =====================================================
# FLUJO DE ANÁLISIS
# =====================================================

st.subheader("🔄 Flujo de Análisis")

st.markdown("""
```text
Eventos
   ↓
Monitoreo
   ↓
Detección de Anomalías
   ↓
Evaluación de Riesgo
   ↓
Threat Intelligence
   ↓
Toma de Decisiones
```
""")

st.divider()

# =====================================================
# OBJETIVOS
# =====================================================

st.subheader("🎯 Objetivos de la Plataforma")

col1, col2, col3 = st.columns(3)

with col1:

    st.success("""
    Detectar comportamientos
    anómalos en usuarios
    y sistemas.
    """)

with col2:

    st.success("""
    Identificar amenazas
    y eventos de riesgo.
    """)

with col3:

    st.success("""
    Apoyar la toma de decisiones
    mediante análisis visual.
    """)

st.divider()

# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Cyber Security Dashboard • Cloud SQL • Streamlit • Python • Threat Intelligence"
)