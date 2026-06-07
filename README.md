# 🛡️ Digital Security Analysis

Plataforma de análisis y monitoreo de eventos de ciberseguridad desarrollada con **Python**, **Streamlit** y **MySQL**, diseñada para centralizar, visualizar y analizar información relacionada con actividades de usuarios, eventos de seguridad, anomalías y niveles de riesgo dentro de un entorno digital.

La solución permite a los analistas explorar grandes volúmenes de información mediante dashboards interactivos, facilitando la identificación de comportamientos sospechosos y apoyando la toma de decisiones basada en datos.

---

# 📖 Descripción del Proyecto

Digital Security Analysis es una aplicación web orientada al análisis de datos de ciberseguridad, construida sobre una arquitectura de visualización con Streamlit y una base de datos MySQL.

El proyecto integra procesos de almacenamiento, consulta y visualización de información relacionada con:

- Actividades de usuarios.
- Eventos de seguridad.
- Acciones realizadas dentro del sistema.
- Detección y clasificación de anomalías.
- Evaluación de riesgos.
- Exploración de registros históricos.

La plataforma proporciona una interfaz intuitiva para el monitoreo y análisis de indicadores clave de seguridad.

---

# 🎯 Objetivos

- Centralizar la información de eventos de seguridad.
- Facilitar el monitoreo continuo de actividades registradas.
- Identificar patrones anómalos dentro de los datos.
- Apoyar la evaluación de riesgos mediante indicadores visuales.
- Proporcionar capacidades de análisis exploratorio para investigadores y analistas.
- Servir como base para futuras implementaciones de detección automática de amenazas mediante Inteligencia Artificial y Machine Learning.

---

# 🏗️ Arquitectura General

```text
Eventos y Registros de Seguridad
                │
                ▼
          Base de Datos
              MySQL
                │
                ▼
          database.py
                │
                ▼
        Consultas SQL
                │
                ▼
             Pandas
                │
                ▼
            Streamlit
                │
 ┌──────────────┼──────────────┐
 ▼              ▼              ▼
Resumen     Monitoreo     Anomalías
 ▼              ▼              ▼
Riesgo      Explorador de Datos
```

---

# 🛠️ Tecnologías Utilizadas

| Tecnología | Descripción |
|------------|-------------|
| Python | Lenguaje principal de desarrollo |
| Streamlit | Framework para dashboards interactivos |
| Pandas | Manipulación y análisis de datos |
| SQLAlchemy | Conexión y gestión de base de datos |
| PyMySQL | Conector MySQL para Python |
| Plotly | Visualización interactiva |
| MySQL | Sistema gestor de bases de datos |
| Google Cloud SQL | Servicio de base de datos administrada |

---

# 📂 Estructura del Proyecto

```text
digital-security-analysis-/

└── streamlit/
    │
    ├── README.md
    │
    └── streamlit/
        │
        ├── app.py
        ├── database.py
        ├── requirements.txt
        │
        ├── .streamlit/
        │   └── secrets.toml
        │
        └── pages/
            ├── 01_Resumen.py
            ├── 02_Monitoreo.py
            ├── 03_Anomalias.py
            ├── 04_Riesgo.py
            └── 05_Explorador.py
```

---

# 📋 Descripción de los Componentes

## app.py

Archivo principal de la aplicación Streamlit.

Responsable de:

- Inicializar la aplicación.
- Configurar la interfaz principal.
- Gestionar la navegación entre páginas.
- Centralizar la experiencia de usuario.

---

## database.py

Módulo encargado de la conexión con la base de datos.

Responsabilidades:

- Crear la conexión a MySQL.
- Ejecutar consultas SQL.
- Obtener información para los dashboards.
- Gestionar la comunicación entre Streamlit y la base de datos.

---

## pages/01_Resumen.py

Dashboard ejecutivo con indicadores generales de seguridad.

Permite:

- Visualizar métricas globales.
- Consultar indicadores clave.
- Obtener una visión general del estado del sistema.

---

## pages/02_Monitoreo.py

Módulo enfocado en el seguimiento de eventos de seguridad.

Permite:

- Supervisar actividades registradas.
- Analizar eventos recientes.
- Identificar comportamientos potencialmente sospechosos.

---

## pages/03_Anomalias.py

Módulo de análisis de anomalías.

Permite:

- Visualizar eventos clasificados como anómalos.
- Analizar tendencias y patrones.
- Facilitar investigaciones de posibles incidentes.

---

## pages/04_Riesgo.py

Módulo de evaluación de riesgo.

Permite:

- Analizar niveles de riesgo asociados a eventos.
- Priorizar incidentes.
- Apoyar procesos de toma de decisiones.

---

## pages/05_Explorador.py

Herramienta de exploración y consulta de datos.

Permite:

- Navegar registros históricos.
- Aplicar filtros y búsquedas.
- Realizar análisis exploratorios.

---

# ⚙️ Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/StefanyLA23/digital-security-analysis-.git
```

---

## 2. Acceder al proyecto Streamlit

```bash
cd digital-security-analysis-
cd streamlit
cd streamlit
```

O directamente:

```bash
cd digital-security-analysis-/streamlit/streamlit
```

---

## 3. Crear entorno virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python -m venv venv
source venv/bin/activate
```

---

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# 🔐 Configuración

La aplicación utiliza un archivo de configuración para almacenar las credenciales de acceso a la base de datos.

Ubicación:

```text
.streamlit/secrets.toml
```

Ejemplo:

```toml
DB_USER = "usuario"
DB_PASSWORD = "contraseña"
DB_HOST = "host"
DB_PORT = "3306"
DB_NAME = "digital_security"
```

> Se recomienda no publicar este archivo en el repositorio para proteger las credenciales.

---

# 🚀 Ejecución

Una vez configuradas las dependencias y credenciales, ejecutar:

```bash
streamlit run app.py
```

La aplicación estará disponible en:

```text
http://localhost:8501
```

---

# 🗄️ Base de Datos

La plataforma utiliza MySQL como sistema gestor de bases de datos para almacenar y consultar información relacionada con:

- Usuarios.
- Eventos de seguridad.
- Registros de actividad.
- Acciones realizadas.
- Anomalías detectadas.
- Evaluaciones de riesgo.

La capa de acceso a datos se encuentra centralizada en el archivo:

```text
database.py
```

---

# 📊 Funcionalidades Principales

✅ Dashboard ejecutivo de seguridad.

✅ Monitoreo de eventos.

✅ Visualización de anomalías.

✅ Evaluación de riesgos.

✅ Exploración interactiva de datos.

✅ Consultas a base de datos en tiempo real.

✅ Visualizaciones analíticas.
