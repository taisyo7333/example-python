FROM registry.redhat.io/ubi9/python-314:latest

WORKDIR /opt/app-root/src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENV PORT=5000
EXPOSE 5000

CMD ["python", "main.py"]
