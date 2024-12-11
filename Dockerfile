# Usar una imagen ligera de Python
FROM python:3.10-slim

# Instalar dependencias del sistema necesarias para mysqlclient y psycopg2-binary
RUN apt-get update && apt-get install -y \
    build-essential \
    libmysqlclient-dev \
    libpq-dev \
    && apt-get clean

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . /app/.

# Crear un entorno virtual e instalar dependencias
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Establecer variables de entorno
ENV PATH="/opt/venv/bin:$PATH"

# Comando para iniciar el servidor
CMD ["gunicorn", "CallCenterGamer.wsgi:application", "--bind", "0.0.0.0:8000"]
