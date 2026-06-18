FROM python:3.10-slim
WORKDIR /app
# requirements.txt is located at the repository root
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
# copy the backend package from the repository into the image
COPY backend/app /app/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
