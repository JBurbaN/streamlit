import streamlit as st
import pandas as pd
import plotly.express as px
from database import query

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Centro de Monitoreo",
    layout="wide"
)

st.title("🖥️ Centro de Monitoreo")

# =====================================================
# CONSULTA PRINCIPAL
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

ORDER BY e.Timestamp
"""

df = query(sql)

# =====================================================
# PREPARACIÓN DE DATOS
# =====================================================

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# =====================================================
# FILTROS
# =====================================================

st.sidebar.header("Filtros")

clasificaciones = st.sidebar.multiselect(
    "Clasificación",
    options=sorted(df["Clasificacion"].dropna().unique()),
    default=sorted(df["Clasificacion"].dropna().unique())
)

anomalias = st.sidebar.multiselect(
    "Anomalía",
    options=sorted(df["Anomalia"].dropna().unique()),
    default=sorted(df["Anomalia"].dropna().unique())
)

actividades = st.sidebar.multiselect(
    "Actividad",
    options=sorted(df["Nombre_Tipo"].dropna().unique()),
    default=sorted(df["Nombre_Tipo"].dropna().unique())
)

df_filtrado = df[
    (df["Clasificacion"].isin(clasificaciones))
    &
    (df["Anomalia"].isin(anomalias))
    &
    (df["Nombre_Tipo"].isin(actividades))
]

# =====================================================
# MÉTRICAS PRINCIPALES
# =====================================================

st.subheader("📊 Estado Actual")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Eventos",
    len(df_filtrado)
)

c2.metric(
    "Usuarios",
    df_filtrado["User_ID"].nunique()
)

c3.metric(
    "IPs",
    df_filtrado["IP_Address"].nunique()
)

promedio_threat = (
    round(df_filtrado["Threat_Score"].mean(), 2)
    if len(df_filtrado) > 0
    else 0
)

c4.metric(
    "Threat Score Promedio",
    promedio_threat
)

# =====================================================
# INDICADORES
# =====================================================

eventos_anomalos = len(
    df_filtrado[
        df_filtrado["Anomalia"] != "Sin anomalía"
    ]
)

if len(df_filtrado) > 0:
    porcentaje = round(
        (eventos_anomalos / len(df_filtrado)) * 100,
        2
    )
else:
    porcentaje = 0

st.info(
    f"🚨 {eventos_anomalos} eventos presentan anomalías ({porcentaje}%)"
)

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
# LÍNEA TEMPORAL
# =====================================================

st.subheader("📈 Línea Temporal de Eventos")

timeline = (
    df_filtrado
    .groupby("Timestamp")
    .size()
    .reset_index(name="Eventos")
)

tab1, tab2, tab3 = st.tabs([
    "Threat Score",
    "Login Attempts",
    "File Size"
])

with tab1:

    fig = px.line(
        df_filtrado.sort_values("Timestamp"),
        x="Timestamp",
        y="Threat_Score",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with tab2:

    fig = px.line(
        df_filtrado.sort_values("Timestamp"),
        x="Timestamp",
        y="Login_Attempts",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with tab3:

    fig = px.line(
        df_filtrado.sort_values("Timestamp"),
        x="Timestamp",
        y="File_Size",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# DISTRIBUCIÓN DE RIESGO
# =====================================================

st.subheader("🏷️ Distribución de Riesgo")

riesgo_chart = (
    df_filtrado
    .groupby("Clasificacion")
    .size()
    .reset_index(name="Total")
)

fig_riesgo = px.pie(
    riesgo_chart,
    names="Clasificacion",
    values="Total",
    hole=0.5
)

st.plotly_chart(
    fig_riesgo,
    use_container_width=True
)

# =====================================================
# ACTIVIDADES Y ACCIONES
# =====================================================

col1, col2 = st.columns(2)

with col1:

    actividades_chart = (
        df_filtrado
        .groupby("Nombre_Tipo")
        .size()
        .reset_index(name="Total")
    )

    fig_actividad = px.bar(
        actividades_chart,
        x="Nombre_Tipo",
        y="Total",
        title="Eventos por Actividad"
    )

    st.plotly_chart(
        fig_actividad,
        use_container_width=True
    )

with col2:

    acciones_chart = (
        df_filtrado
        .groupby("Nombre_Accion")
        .size()
        .reset_index(name="Total")
    )

    fig_accion = px.bar(
        acciones_chart,
        x="Nombre_Accion",
        y="Total",
        title="Eventos por Acción"
    )

    st.plotly_chart(
        fig_accion,
        use_container_width=True
    )

st.divider()

# =====================================================
# USUARIOS MÁS ACTIVOS
# =====================================================

st.subheader("👤 Usuarios con Más Actividad")

usuarios_chart = (
    df_filtrado
    .groupby("User_ID")
    .size()
    .reset_index(name="Eventos")
    .sort_values(
        by="Eventos",
        ascending=False
    )
)

fig_users = px.bar(
    usuarios_chart,
    x="User_ID",
    y="Eventos",
    title="Actividad por Usuario"
)

st.plotly_chart(
    fig_users,
    use_container_width=True
)

# =====================================================
# ACTIVIDAD POR IP
# =====================================================

st.subheader("🌐 Actividad por Dirección IP")

ip_chart = (
    df_filtrado
    .groupby("IP_Address")
    .size()
    .reset_index(name="Eventos")
)

fig_ip = px.bar(
    ip_chart,
    x="IP_Address",
    y="Eventos",
    title="Eventos por Dirección IP"
)

st.plotly_chart(
    fig_ip,
    use_container_width=True
)

st.divider()

# =====================================================
# LOGIN ATTEMPTS
# =====================================================

st.subheader("🔐 Intentos de Inicio de Sesión")

fig_login = px.bar(
    df_filtrado,
    x="ID_Evento",
    y="Login_Attempts",
    color="Clasificacion",
    title="Intentos de Login por Evento"
)

st.plotly_chart(
    fig_login,
    use_container_width=True
)

# =====================================================
# FILE SIZE
# =====================================================

st.subheader("📁 Transferencia de Archivos")

fig_files = px.bar(
    df_filtrado,
    x="ID_Evento",
    y="File_Size",
    color="Clasificacion",
    title="Tamaño de Archivo por Evento"
)

st.plotly_chart(
    fig_files,
    use_container_width=True
)

st.divider()

# =====================================================
# HEATMAP DE RIESGO
# =====================================================

st.subheader("🔥 Mapa de Riesgo")

heatmap = (
    df_filtrado
    .groupby(
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
    title="Mapa de Riesgo por Clasificación y Anomalía"
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)

# =====================================================
# TOP EVENTOS DE RIESGO
# =====================================================

st.subheader("🚨 Eventos de Mayor Riesgo")

top_riesgo = (
    df_filtrado
    .sort_values(
        by="Threat_Score",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_riesgo[
        [
            "ID_Evento",
            "User_ID",
            "IP_Address",
            "Nombre_Tipo",
            "Anomalia",
            "Clasificacion",
            "Login_Attempts",
            "Threat_Score"
        ]
    ],
    use_container_width=True,
    hide_index=True,
    column_config={
        "Threat_Score": st.column_config.ProgressColumn(
            "Threat Score",
            min_value=0,
            max_value=max(
                int(df_filtrado["Threat_Score"].max()),
                200
            ) if len(df_filtrado) > 0 else 200
        )
    }
)

st.divider()

# =====================================================
# TABLA GENERAL
# =====================================================

st.subheader("📋 Eventos Registrados")

st.dataframe(
    df_filtrado,
    use_container_width=True,
    hide_index=True
)

st.divider()

# =====================================================
# RECOMENDACIONES
# =====================================================

st.subheader("💡 Recomendaciones")

if promedio_threat >= 100:

    st.error(
        """
        Revisar inmediatamente los eventos
        clasificados como Alto Riesgo.
        """
    )

elif promedio_threat >= 70:

    st.warning(
        """
        Mantener monitoreo constante sobre
        usuarios y actividades sospechosas.
        """
    )

else:

    st.success(
        """
        No se identifican riesgos relevantes.
        """
    )