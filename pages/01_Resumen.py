import streamlit as st
import pandas as pd
import plotly.express as px
from database import query

st.set_page_config(
page_title="Resumen Ejecutivo",
layout="wide"
)

st.title("🛡️ Resumen Ejecutivo")

total_eventos = query("""
SELECT COUNT(*) AS total
FROM Evento
""").iloc[0]["total"]

usuarios_activos = query("""
SELECT COUNT(DISTINCT ID_Usuario) AS total
FROM Evento
""").iloc[0]["total"]

anomalias = query("""
SELECT COUNT(*) AS total
FROM Evento
WHERE ID_Anomalia <> 0
""").iloc[0]["total"]

alto_riesgo = query("""
SELECT COUNT(*) AS total
FROM Evento
WHERE ID_Clasificacion = 3
""").iloc[0]["total"]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
"📊 Total Eventos",
total_eventos
)

col2.metric(
"👤 Usuarios Activos",
usuarios_activos
)

col3.metric(
"🚨 Eventos con Anomalías",
anomalias
)

col4.metric(
"⚠️ Eventos Alto Riesgo",
alto_riesgo
)

st.divider()

st.subheader("🏷️ Distribución por Nivel de Riesgo")

riesgo = query("""
SELECT
c.Etiqueta,
COUNT(*) AS Total
FROM Evento e
INNER JOIN Clasificacion c
ON e.ID_Clasificacion = c.ID_Clasificacion
GROUP BY c.Etiqueta
""")

fig_riesgo = px.pie(
riesgo,
names="Etiqueta",
values="Total",
title="Clasificación de Riesgo"
)

st.plotly_chart(
fig_riesgo,
use_container_width=True
)

st.divider()

st.subheader("🚨 Distribución de Anomalías")

anomalias_df = query("""
SELECT
a.Descripcion,
COUNT(*) AS Total
FROM Evento e
INNER JOIN Anomalia a
ON e.ID_Anomalia = a.ID_Anomalia
GROUP BY a.Descripcion
ORDER BY Total DESC
""")

fig_anomalias = px.bar(
anomalias_df,
x="Descripcion",
y="Total",
title="Eventos por Tipo de Anomalía"
)

st.plotly_chart(
fig_anomalias,
use_container_width=True
)

st.divider()

st.subheader("📁 Actividades Registradas")

actividades = query("""
SELECT
ta.Nombre_Tipo,
COUNT(*) AS Total
FROM Evento e
INNER JOIN TipoActividad ta
ON e.ID_TipoActividad = ta.ID_TipoActividad
GROUP BY ta.Nombre_Tipo
ORDER BY Total DESC
""")

fig_actividades = px.bar(
actividades,
x="Nombre_Tipo",
y="Total",
title="Eventos por Tipo de Actividad"
)

st.plotly_chart(
fig_actividades,
use_container_width=True
)

st.divider()

st.subheader("🔐 Intentos de Inicio de Sesión")

login_df = query("""
SELECT
ID_Evento,
Login_Attempts
FROM Evento
ORDER BY ID_Evento
""")

fig_login = px.bar(
login_df,
x="ID_Evento",
y="Login_Attempts",
title="Intentos de Login por Evento"
)

st.plotly_chart(
fig_login,
use_container_width=True
)

st.divider()

st.subheader("🎯 Indicador de Amenaza")

threat_df = query("""
SELECT
ID_Evento,
(
(ID_Clasificacion * 30)
+
(ID_Anomalia * 20)
+
(Login_Attempts * 5)
) AS Threat_Score
FROM Evento
""")

promedio = round(
threat_df["Threat_Score"].mean(),
2
)

maximo = round(
threat_df["Threat_Score"].max(),
2
)

c1, c2 = st.columns(2)

c1.metric(
"Threat Score Promedio",
promedio
)

c2.metric(
"Threat Score Máximo",
maximo
)

fig_threat = px.bar(
threat_df,
x="ID_Evento",
y="Threat_Score",
title="Threat Score por Evento"
)

st.plotly_chart(
fig_threat,
use_container_width=True
)

st.success(
"Dashboard conectado exitosamente a Google Cloud SQL."
)