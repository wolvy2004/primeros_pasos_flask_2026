FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
#CMD ["flask", "--app", "app.py", "run", "--debug", "--host=0.0.0.0"]
CMD ["flask", "--app", "App", "run", "--debug", "--host=0.0.0.0"]
