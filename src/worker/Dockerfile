FROM python:3.8-alpine
USER root
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
EXPOSE 8082
# ENTRYPOINT ["python","-u", "model_server.py"]
CMD [ "python", "worker.py" ]