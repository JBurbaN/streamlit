import streamlit as st
import pandas as pd
import plotly.express as px
from database import query

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Explorador de Eventos",
    layout="wide"
)

st.title("🔎 Explorador de Eventos")

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

ORDER BY e.ID_Evento
"""

df = query(sql)

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# =====================================================
# FILTROS
# =====================================================

st.sidebar.header("Filtros")

usuario = st.sidebar.selectbox(
    "Usuario",
    ["Todos"] + sorted(
        df["User_ID"].astype(str).unique().tolist()
    )
)

clasificacion = st.sidebar.selectbox(
    "Clasificación",
    ["Todas"] + sorted(
        df["Clasificacion"].dropna().unique().tolist()
    )
)

anomalia = st.sidebar.selectbox(
    "Anomalía",
    ["Todas"] + sorted(
        df["Anomalia"].dropna().unique().tolist()
    )
)

actividad = st.sidebar.selectbox(
    "Actividad",
    ["Todas"] + sorted(
        df["Nombre_Tipo"].dropna().unique().tolist()
    )
)

# =====================================================
# FILTROS AVANZADOS
# =====================================================

threat_min = st.sidebar.slider(
    "Threat Score mínimo",
    min_value=0,
    max_value=200,
    value=0
)

# =====================================================
# APLICAR FILTROS
# =====================================================

if usuario != "Todos":
    df = df[
        df["User_ID"].astype(str) == usuario
    ]

if clasificacion != "Todas":
    df = df[
        df["Clasificacion"] == clasificacion
    ]

if anomalia != "Todas":
    df = df[
        df["Anomalia"] == anomalia
    ]

if actividad != "Todas":
    df = df[
        df["Nombre_Tipo"] == actividad
    ]

df = df[
    df["Threat_Score"] >= threat_min
]

# =====================================================
# BÚSQUEDA GLOBAL
# =====================================================

st.subheader("🔍 Búsqueda Inteligente")

texto = st.text_input(
    "Buscar por usuario, IP, actividad, acción o anomalía"
)

if texto:

    texto = texto.lower()

    df = df[
        df.astype(str)
        .apply(
            lambda row:
            row.str.lower().str.contains(texto).any(),
            axis=1
        )
    ]

# =====================================================
# KPIs
# =====================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Eventos",
    len(df)
)

c2.metric(
    "Usuarios",
    df["User_ID"].nunique()
)

c3.metric(
    "IPs",
    df["IP_Address"].nunique()
)

c4.metric(
    "Threat Score Promedio",
    round(
        df["Threat_Score"].mean(),
        2
    ) if len(df) > 0 else 0
)

# =====================================================
# ALERTA
# =====================================================

if len(df) > 0:

    threat_promedio = round(
        df["Threat_Score"].mean(),
        2
    )

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
# VISUALIZACIONES
# =====================================================

if len(df) > 0:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📊 Distribución de Riesgo")

        fig_riesgo = px.pie(
            df,
            names="Clasificacion",
            title="Clasificación de Riesgo"
        )

        st.plotly_chart(
            fig_riesgo,
            use_container_width=True
        )

    with col2:

        st.subheader("📈 Threat Score")

        fig_score = px.line(
            df.sort_values("Timestamp"),
            x="Timestamp",
            y="Threat_Score",
            markers=True
        )

        st.plotly_chart(
            fig_score,
            use_container_width=True
        )

st.divider()

# =====================================================
# TABLA PRINCIPAL
# =====================================================

st.subheader("📋 Eventos Encontrados")

st.dataframe(
    df,
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

# =====================================================
# DETALLE DE EVENTO
# =====================================================

if len(df) > 0:

    st.divider()

    st.subheader("📝 Detalle de Evento")

    evento = st.selectbox(
        "Seleccione un Evento",
        df["ID_Evento"]
    )

    detalle = df[
        df["ID_Evento"] == evento
    ].iloc[0]

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 📌 Información General")

        st.write(
            f"**Evento:** {detalle['ID_Evento']}"
        )

        st.write(
            f"**Usuario:** {detalle['User_ID']}"
        )

        st.write(
            f"**IP:** {detalle['IP_Address']}"
        )

        st.write(
            f"**Fecha:** {detalle['Timestamp']}"
        )

        st.write(
            f"**Actividad:** {detalle['Nombre_Tipo']}"
        )

        st.write(
            f"**Acción:** {detalle['Nombre_Accion']}"
        )

    with col2:

        st.markdown("### 🔐 Información de Seguridad")

        st.write(
            f"**Anomalía:** {detalle['Anomalia']}"
        )

        st.write(
            f"**Clasificación:** {detalle['Clasificacion']}"
        )

        st.write(
            f"**Login Attempts:** {detalle['Login_Attempts']}"
        )

        st.write(
            f"**File Size:** {detalle['File_Size']}"
        )

        st.write(
            f"**Threat Score:** {detalle['Threat_Score']}"
        )

# =====================================================
# EXPORTACIÓN
# =====================================================

st.divider()

csv = df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Descargar CSV",
    data=csv,
    file_name="eventos_filtrados.csv",
    mime="text/csv"
)

# =====================================================
# ESTADÍSTICAS
# =====================================================

st.divider()

st.subheader("📊 Estadísticas")

if len(df) > 0:

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Threat Score Máximo",
        round(
            df["Threat_Score"].max(),
            2
        )
    )

    c2.metric(
        "Threat Score Mínimo",
        round(
            df["Threat_Score"].min(),
            2
        )
    )

    c3.metric(
        "Threat Score Promedio",
        round(
            df["Threat_Score"].mean(),
            2
        )
    )

    st.subheader("🏆 Top 5 Eventos Más Riesgosos")

    top5 = (
        df.sort_values(
            by="Threat_Score",
            ascending=False
        )
        .head(5)
    )

    st.dataframe(
        top5[
            [
                "ID_Evento",
                "User_ID",
                "Anomalia",
                "Clasificacion",
                "Threat_Score"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "No existen registros para los filtros seleccionados."
    )