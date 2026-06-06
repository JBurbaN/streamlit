import streamlit as st
import pandas as pd
import plotly.express as px
from database import query

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Análisis de Riesgo",
    layout="wide"
)

st.title("⚠️ Análisis de Riesgo")

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
# CLASIFICACIÓN DE RIESGO
# =====================================================

def nivel_riesgo(score):

    if score < 60:
        return "Bajo"

    elif score < 100:
        return "Medio"

    return "Alto"

df["Nivel_Riesgo"] = df["Threat_Score"].apply(
    nivel_riesgo
)

# =====================================================
# FILTROS
# =====================================================

st.sidebar.header("Filtros")

riesgos = st.sidebar.multiselect(
    "Nivel de Riesgo",
    options=sorted(df["Nivel_Riesgo"].unique()),
    default=sorted(df["Nivel_Riesgo"].unique())
)

clasificaciones = st.sidebar.multiselect(
    "Clasificación",
    options=sorted(df["Clasificacion"].dropna().unique()),
    default=sorted(df["Clasificacion"].dropna().unique())
)

df = df[
    (df["Nivel_Riesgo"].isin(riesgos))
    &
    (df["Clasificacion"].isin(clasificaciones))
]

# =====================================================
# KPIs
# =====================================================

total = len(df)

riesgo_alto = len(
    df[df["Nivel_Riesgo"] == "Alto"]
)

riesgo_medio = len(
    df[df["Nivel_Riesgo"] == "Medio"]
)

riesgo_bajo = len(
    df[df["Nivel_Riesgo"] == "Bajo"]
)

promedio_threat = (
    round(df["Threat_Score"].mean(), 2)
    if len(df) > 0
    else 0
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Eventos Analizados",
    total
)

c2.metric(
    "🔴 Riesgo Alto",
    riesgo_alto
)

c3.metric(
    "🟠 Riesgo Medio",
    riesgo_medio
)

c4.metric(
    "🟢 Riesgo Bajo",
    riesgo_bajo
)

# =====================================================
# ALERTA GENERAL
# =====================================================

if promedio_threat >= 100:

    st.error(
        f"🔴 Riesgo Alto Detectado ({promedio_threat})"
    )

elif promedio_threat >= 70:

    st.warning(
        f"🟠 Riesgo Medio Detectado ({promedio_threat})"
    )

else:

    st.success(
        f"🟢 Riesgo Bajo ({promedio_threat})"
    )

st.divider()

# =====================================================
# DISTRIBUCIÓN DEL RIESGO
# =====================================================

st.subheader("📊 Distribución del Riesgo")

riesgo = (
    df.groupby("Nivel_Riesgo")
    .size()
    .reset_index(name="Total")
)

fig_riesgo = px.pie(
    riesgo,
    names="Nivel_Riesgo",
    values="Total",
    hole=0.5,
    title="Distribución de Eventos por Riesgo"
)

st.plotly_chart(
    fig_riesgo,
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
    color="Nivel_Riesgo",
    markers=True,
    title="Evolución Temporal del Riesgo"
)

st.plotly_chart(
    fig_timeline,
    use_container_width=True
)

st.divider()

# =====================================================
# THREAT SCORE POR EVENTO
# =====================================================

st.subheader("🎯 Threat Score por Evento")

fig_score = px.bar(
    df,
    x="ID_Evento",
    y="Threat_Score",
    color="Nivel_Riesgo",
    text="Threat_Score",
    title="Puntaje de Amenaza"
)

st.plotly_chart(
    fig_score,
    use_container_width=True
)

st.divider()

# =====================================================
# RIESGO POR USUARIO
# =====================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("👤 Riesgo por Usuario")

    riesgo_usuario = (
        df.groupby("User_ID")
        .agg({
            "Threat_Score": "mean"
        })
        .reset_index()
        .sort_values(
            by="Threat_Score",
            ascending=False
        )
    )

    fig_usuario = px.bar(
        riesgo_usuario,
        x="User_ID",
        y="Threat_Score",
        title="Promedio de Riesgo por Usuario"
    )

    st.plotly_chart(
        fig_usuario,
        use_container_width=True
    )

with col2:

    st.subheader("🌐 Riesgo por Dirección IP")

    riesgo_ip = (
        df.groupby("IP_Address")
        .agg({
            "Threat_Score": "mean"
        })
        .reset_index()
        .sort_values(
            by="Threat_Score",
            ascending=False
        )
    )

    fig_ip = px.bar(
        riesgo_ip,
        x="IP_Address",
        y="Threat_Score",
        title="Promedio de Riesgo por IP"
    )

    st.plotly_chart(
        fig_ip,
        use_container_width=True
    )

st.divider()

# =====================================================
# LOGIN ATTEMPTS VS RIESGO
# =====================================================

st.subheader("🔐 Login Attempts y Riesgo")

fig_login = px.scatter(
    df,
    x="Login_Attempts",
    y="Threat_Score",
    color="Nivel_Riesgo",
    size="File_Size",
    hover_data=[
        "User_ID",
        "Anomalia",
        "Clasificacion"
    ],
    title="Intentos de Login vs Riesgo"
)

st.plotly_chart(
    fig_login,
    use_container_width=True
)

# =====================================================
# FILE SIZE VS RIESGO
# =====================================================

st.subheader("📁 Tamaño de Archivos y Riesgo")

fig_files = px.scatter(
    df,
    x="File_Size",
    y="Threat_Score",
    color="Nivel_Riesgo",
    hover_data=[
        "User_ID",
        "Anomalia"
    ],
    title="File Size vs Threat Score"
)

st.plotly_chart(
    fig_files,
    use_container_width=True
)

st.divider()

# =====================================================
# MAPA DE RIESGO
# =====================================================

st.subheader("🔥 Mapa de Riesgo")

heatmap = (
    df.groupby(
        ["Nivel_Riesgo", "Anomalia"]
    )
    .size()
    .reset_index(name="Total")
)

fig_heatmap = px.density_heatmap(
    heatmap,
    x="Nivel_Riesgo",
    y="Anomalia",
    z="Total",
    title="Nivel de Riesgo vs Anomalía"
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)

st.divider()

# =====================================================
# TOP EVENTOS DE MAYOR RIESGO
# =====================================================

st.subheader("🚨 Top Eventos de Mayor Riesgo")

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
            "Threat_Score",
            "Nivel_Riesgo"
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

if riesgo_alto > 0:

    st.error(
        f"""
        Se detectaron {riesgo_alto} eventos de riesgo alto.
        Se recomienda revisión inmediata.
        """
    )

if riesgo_medio > 0:

    st.warning(
        f"""
        Se detectaron {riesgo_medio} eventos de riesgo medio.
        Mantener monitoreo continuo.
        """
    )

if riesgo_alto == 0 and riesgo_medio == 0:

    st.success(
        """
        No se detectaron eventos de riesgo significativo.
        """
    )