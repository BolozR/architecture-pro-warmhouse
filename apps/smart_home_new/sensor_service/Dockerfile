FROM python:3.8-slim
WORKDIR /sensor_service
COPY . /sensor_service
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8082
CMD ["python", "main.py"]