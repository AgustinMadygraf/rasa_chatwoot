# Imagen base de Python
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el codigo de la aplicacion
COPY . .

# Exponer el puerto (variable de entorno)
EXPOSE ${PORT:-8000}

# Comando para ejecutar la aplicacion
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
