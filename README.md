# Digital Security Analysis

Digital Security Analysis es una aplicación web desarrollada con Streamlit para el análisis y monitoreo de eventos de ciberseguridad almacenados en una base de datos MySQL. La plataforma permite visualizar indicadores clave, monitorear actividades registradas, analizar anomalías y explorar información relacionada con riesgos de seguridad mediante dashboards interactivos.

## Tecnologías utilizadas

- Python
- Streamlit
- Pandas
- Plotly
- SQLAlchemy
- PyMySQL
- MySQL
- Google Cloud SQL

## Estructura del proyecto

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

## Módulos

### Resumen

Presenta una vista general de los principales indicadores de seguridad obtenidos desde la base de datos.

### Monitoreo

Permite consultar y visualizar eventos registrados para realizar seguimiento a la actividad del sistema.

### Anomalías

Muestra información relacionada con eventos clasificados como anómalos para facilitar su análisis.

### Riesgo

Proporciona una vista enfocada en la evaluación y priorización de riesgos identificados.

### Explorador

Permite navegar y consultar los datos almacenados mediante filtros y visualizaciones interactivas.

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/StefanyLA23/digital-security-analysis-.git
```

Ingresar a la aplicación:

```bash
cd digital-security-analysis-
cd streamlit
cd streamlit
```

Crear un entorno virtual:

```bash
python -m venv venv
```

Activar el entorno:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

Crear o actualizar el archivo:

```text
.streamlit/secrets.toml
```

Con las credenciales de conexión a la base de datos:

```toml
DB_USER = "usuario"
DB_PASSWORD = "contraseña"
DB_HOST = "host"
DB_PORT = "3306"
DB_NAME = "nombre_base_datos"
```

## Ejecución

Desde la carpeta donde se encuentra `app.py`:

```bash
streamlit run app.py
```

La aplicación estará disponible en:

```text
http://localhost:8501
```

## Base de datos

La aplicación utiliza MySQL como fuente principal de información. La conexión y las consultas necesarias para alimentar los dashboards se gestionan desde el archivo `database.py`.
