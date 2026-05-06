FROM python:3.8-slim
WORKDIR /telemetry_service
COPY . /telemetry_service
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8083
CMD ["python", "main.py"]