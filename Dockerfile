# Usa la imagen base de Python 3 slim
FROM python:3.9-slim

# Establece el directorio de trabajo en /programas/api-clients
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt .


# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt\
    && pip3 install pydantic \
    && pip3 install "fastapi[standard]" \
    && pip3 install pydantic \
    && pip3 install psycopg2-binary

# Copia todos los archivos al contenedor
COPY . .

# Expone el puerto 8000
EXPOSE 8002

# Comando para ejecutar la aplicación FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8002"]

