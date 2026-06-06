import streamlit as st
import pandas as pd
import plotly.express as px
from database import query

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Threat Intelligence",
    layout="wide"
)

st.title("🕵️ Threat Intelligence Center")

st.markdown("""
Centro de inteligencia de amenazas para identificar
usuarios, IPs, actividades y eventos con mayor nivel
de riesgo dentro del sistema.
""")

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
# NIVEL DE RIESGO
# =====================================================

def clasificar_riesgo(score):

    if score < 60:
        return "Bajo"

    elif score < 100:
        return "Medio"

    return "Alto"

df["Nivel_Riesgo"] = df["Threat_Score"].apply(
    clasificar_riesgo
)

# =====================================================
# KPIs PRINCIPALES
# =====================================================

st.subheader("📊 Indicadores Estratégicos")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Eventos Analizados",
    len(df)
)

c2.metric(
    "Threat Score Máximo",
    round(df["Threat_Score"].max(), 2)
)

c3.metric(
    "Threat Score Promedio",
    round(df["Threat_Score"].mean(), 2)
)

c4.metric(
    "Usuarios Únicos",
    df["User_ID"].nunique()
)

st.divider()

# =====================================================
# TOP EVENTOS
# =====================================================

st.subheader("🚨 Top 10 Eventos Más Críticos")

top_eventos = (
    df.sort_values(
        by="Threat_Score",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_eventos[
        [
            "ID_Evento",
            "User_ID",
            "IP_Address",
            "Anomalia",
            "Clasificacion",
            "Threat_Score"
        ]
    ],
    use_container_width=True,
    hide_index=True,
    column_config={
        "Threat_Score":
        st.column_config.ProgressColumn(
            "Threat Score",
            min_value=0,
            max_value=200
        )
    }
)

st.divider()

# =====================================================
# USUARIOS MÁS RIESGOSOS
# =====================================================

st.subheader("👤 Usuarios con Mayor Riesgo")

usuarios = (
    df.groupby("User_ID")
    .agg(
        Eventos=("ID_Evento", "count"),
        Threat_Promedio=("Threat_Score", "mean"),
        Threat_Maximo=("Threat_Score", "max")
    )
    .reset_index()
    .sort_values(
        by="Threat_Promedio",
        ascending=False
    )
)

fig_users = px.bar(
    usuarios,
    x="User_ID",
    y="Threat_Promedio",
    color="Threat_Maximo",
    title="Usuarios con Mayor Riesgo"
)

st.plotly_chart(
    fig_users,
    use_container_width=True
)

st.dataframe(
    usuarios,
    use_container_width=True,
    hide_index=True
)

st.divider()

# =====================================================
# IPS SOSPECHOSAS
# =====================================================

st.subheader("🌐 Direcciones IP Sospechosas")

ips = (
    df.groupby("IP_Address")
    .agg(
        Eventos=("ID_Evento", "count"),
        Threat_Promedio=("Threat_Score", "mean"),
        Threat_Maximo=("Threat_Score", "max")
    )
    .reset_index()
    .sort_values(
        by="Threat_Promedio",
        ascending=False
    )
)

fig_ips = px.bar(
    ips,
    x="IP_Address",
    y="Threat_Promedio",
    color="Threat_Maximo",
    title="IPs con Mayor Riesgo"
)

st.plotly_chart(
    fig_ips,
    use_container_width=True
)

st.divider()

# =====================================================
# ACTIVIDADES MÁS PELIGROSAS
# =====================================================

st.subheader("📁 Actividades Más Riesgosas")

actividades = (
    df.groupby("Nombre_Tipo")
    .agg(
        Eventos=("ID_Evento", "count"),
        Threat_Promedio=("Threat_Score", "mean")
    )
    .reset_index()
    .sort_values(
        by="Threat_Promedio",
        ascending=False
    )
)

fig_actividades = px.bar(
    actividades,
    x="Nombre_Tipo",
    y="Threat_Promedio",
    title="Threat Score Promedio por Actividad"
)

st.plotly_chart(
    fig_actividades,
    use_container_width=True
)

st.divider()

# =====================================================
# ACCIONES MÁS PELIGROSAS
# =====================================================

st.subheader("⚙️ Acciones Más Riesgosas")

acciones = (
    df.groupby("Nombre_Accion")
    .agg(
        Eventos=("ID_Evento", "count"),
        Threat_Promedio=("Threat_Score", "mean")
    )
    .reset_index()
    .sort_values(
        by="Threat_Promedio",
        ascending=False
    )
)

fig_acciones = px.bar(
    acciones,
    x="Nombre_Accion",
    y="Threat_Promedio",
    title="Threat Score Promedio por Acción"
)

st.plotly_chart(
    fig_acciones,
    use_container_width=True
)

st.divider()

# =====================================================
# MATRIZ DE AMENAZAS
# =====================================================

st.subheader("🔥 Matriz de Amenazas")

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
# INTELIGENCIA TEMPORAL
# =====================================================

st.subheader("📈 Evolución del Riesgo")

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
# RECOMENDACIONES AUTOMÁTICAS
# =====================================================

st.subheader("🧠 Inteligencia y Recomendaciones")

max_score = df["Threat_Score"].max()

if max_score >= 120:

    st.error("""
    Se identificaron eventos críticos.
    Recomendación:
    
    • Revisar usuarios involucrados.
    • Auditar accesos recientes.
    • Validar actividades sospechosas.
    • Analizar origen de direcciones IP.
    """)

elif max_score >= 80:

    st.warning("""
    Se identificaron eventos de riesgo medio.

    • Mantener monitoreo continuo.
    • Revisar actividad de usuarios.
    • Analizar intentos de autenticación.
    """)

else:

    st.success("""
    No se identifican amenazas críticas
    en el conjunto de datos analizado.
    """)

st.divider()

# =====================================================
# RESUMEN EJECUTIVO
# =====================================================

st.subheader("📄 Resumen Ejecutivo")

st.info(
    f"""
    • Eventos analizados: {len(df)}

    • Usuarios únicos: {df['User_ID'].nunique()}

    • IPs únicas: {df['IP_Address'].nunique()}

    • Threat Score promedio: {round(df['Threat_Score'].mean(), 2)}

    • Threat Score máximo: {round(df['Threat_Score'].max(), 2)}
    """
)