import streamlit as st
import pandas as pd
import plotly.express as px
from database import query

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Análisis de Anomalías",
    layout="wide"
)

st.title("🚨 Análisis de Anomalías")

# =====================================================
# CONSULTA
# =====================================================

sql = """
SELECT

    e.ID_Evento,
    e.Timestamp,

    u.User_ID,
    u.IP_Address,

    ta.Nombre_Tipo,
    a.Nombre_Accion,

    an.Descripcion AS Anomalia,

    c.Etiqueta AS Clasificacion,

    e.Login_Attempts,
    e.File_Size,

    (
        (e.ID_Clasificacion * 30)
        +
        (e.ID_Anomalia * 20)
        +
        (e.Login_Attempts * 5)
    ) AS Threat_Score

FROM Evento e

LEFT JOIN Usuario u
    ON e.ID_Usuario = u.ID_Usuario

LEFT JOIN TipoActividad ta
    ON e.ID_TipoActividad = ta.ID_TipoActividad

LEFT JOIN Accion a
    ON e.ID_Accion = a.ID_Accion

LEFT JOIN Anomalia an
    ON e.ID_Anomalia = an.ID_Anomalia

LEFT JOIN Clasificacion c
    ON e.ID_Clasificacion = c.ID_Clasificacion
"""

df = query(sql)

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# =====================================================
# FILTROS
# =====================================================

st.sidebar.header("Filtros")

anomalias_filtro = st.sidebar.multiselect(
    "Anomalías",
    options=sorted(df["Anomalia"].dropna().unique()),
    default=sorted(df["Anomalia"].dropna().unique())
)

clasificaciones_filtro = st.sidebar.multiselect(
    "Clasificación",
    options=sorted(df["Clasificacion"].dropna().unique()),
    default=sorted(df["Clasificacion"].dropna().unique())
)

df = df[
    (df["Anomalia"].isin(anomalias_filtro))
    &
    (df["Clasificacion"].isin(clasificaciones_filtro))
]

# =====================================================
# KPIs
# =====================================================

total_eventos = len(df)

eventos_anomalos = len(
    df[df["Anomalia"] != "Normal"]
)

threat_promedio = (
    round(df["Threat_Score"].mean(), 2)
    if len(df) > 0
    else 0
)

threat_maximo = (
    round(df["Threat_Score"].max(), 2)
    if len(df) > 0
    else 0
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Eventos Analizados",
    total_eventos
)

c2.metric(
    "Eventos con Anomalía",
    eventos_anomalos
)

c3.metric(
    "Threat Score Promedio",
    threat_promedio
)

c4.metric(
    "Threat Score Máximo",
    threat_maximo
)

# =====================================================
# ALERTA DE RIESGO
# =====================================================

if threat_promedio >= 100:

    st.error(
        f"🔴 Riesgo Alto Detectado ({threat_promedio})"
    )

elif threat_promedio >= 70:

    st.warning(
        f"🟠 Riesgo Medio Detectado ({threat_promedio})"
    )

else:

    st.success(
        f"🟢 Riesgo Bajo ({threat_promedio})"
    )

st.divider()

# =====================================================
# DISTRIBUCIÓN DE ANOMALÍAS
# =====================================================

st.subheader("📊 Distribución de Anomalías")

anomalias = (
    df.groupby("Anomalia")
    .size()
    .reset_index(name="Total")
)

fig_anomalias = px.bar(
    anomalias,
    x="Anomalia",
    y="Total",
    text="Total",
    color="Total",
    title="Frecuencia de Anomalías"
)

st.plotly_chart(
    fig_anomalias,
    use_container_width=True
)

# =====================================================
# EVOLUCIÓN TEMPORAL
# =====================================================

st.subheader("📈 Evolución del Threat Score")

fig_timeline = px.line(
    df.sort_values("Timestamp"),
    x="Timestamp",
    y="Threat_Score",
    color="Clasificacion",
    markers=True,
    title="Evolución Temporal del Riesgo"
)

st.plotly_chart(
    fig_timeline,
    use_container_width=True
)

# =====================================================
# RIESGO Y ACTIVIDAD
# =====================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("⚠️ Clasificación de Riesgo")

    riesgo = (
        df.groupby("Clasificacion")
        .size()
        .reset_index(name="Total")
    )

    fig_riesgo = px.pie(
        riesgo,
        names="Clasificacion",
        values="Total",
        hole=0.5
    )

    st.plotly_chart(
        fig_riesgo,
        use_container_width=True
    )

with col2:

    st.subheader("📁 Anomalías por Actividad")

    actividad = (
        df.groupby(
            ["Nombre_Tipo", "Anomalia"]
        )
        .size()
        .reset_index(name="Total")
    )

    fig_actividad = px.bar(
        actividad,
        x="Nombre_Tipo",
        y="Total",
        color="Anomalia",
        barmode="group"
    )

    st.plotly_chart(
        fig_actividad,
        use_container_width=True
    )

st.divider()

# =====================================================
# MAPA DE RIESGO
# =====================================================

st.subheader("🔥 Mapa de Riesgo")

heatmap = (
    df.groupby(
        ["Clasificacion", "Anomalia"]
    )
    .size()
    .reset_index(name="Total")
)

fig_heatmap = px.density_heatmap(
    heatmap,
    x="Clasificacion",
    y="Anomalia",
    z="Total",
    title="Clasificación vs Anomalía"
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)

st.divider()

# =====================================================
# LOGIN ATTEMPTS
# =====================================================

st.subheader("🔐 Login Attempts vs Threat Score")

fig_login = px.scatter(
    df,
    x="Login_Attempts",
    y="Threat_Score",
    color="Clasificacion",
    size="File_Size",
    hover_data=[
        "User_ID",
        "IP_Address",
        "Anomalia"
    ],
    title="Intentos de Login y Riesgo"
)

st.plotly_chart(
    fig_login,
    use_container_width=True
)

st.divider()

# =====================================================
# USUARIOS MÁS RIESGOSOS
# =====================================================

st.subheader("👤 Usuarios con Mayor Riesgo")

usuarios = (
    df.groupby("User_ID")
    ["Threat_Score"]
    .mean()
    .reset_index()
    .sort_values(
        by="Threat_Score",
        ascending=False
    )
)

fig_users = px.bar(
    usuarios,
    x="User_ID",
    y="Threat_Score",
    title="Threat Score Promedio por Usuario"
)

st.plotly_chart(
    fig_users,
    use_container_width=True
)

st.divider()

# =====================================================
# EVENTOS MÁS RIESGOSOS
# =====================================================

st.subheader("🚨 Top Eventos Más Riesgosos")

top = (
    df.sort_values(
        by="Threat_Score",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top[
        [
            "ID_Evento",
            "User_ID",
            "IP_Address",
            "Anomalia",
            "Clasificacion",
            "Login_Attempts",
            "File_Size",
            "Threat_Score"
        ]
    ],
    use_container_width=True,
    hide_index=True,
    column_config={
        "Threat_Score": st.column_config.ProgressColumn(
            "Threat Score",
            min_value=0,
            max_value=200
        )
    }
)

st.divider()

# =====================================================
# DETALLE DE EVENTOS
# =====================================================

st.subheader("📋 Detalle de Eventos")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# =====================================================
# RECOMENDACIONES
# =====================================================

st.subheader("💡 Recomendaciones")

if threat_promedio >= 100:

    st.error(
        """
        Revisar inmediatamente los eventos
        clasificados como Alto Riesgo.
        """
    )

elif threat_promedio >= 70:

    st.warning(
        """
        Mantener monitoreo continuo de usuarios
        y anomalías detectadas.
        """
    )

else:

    st.success(
        """
        No se identifican anomalías críticas.
        """
    )