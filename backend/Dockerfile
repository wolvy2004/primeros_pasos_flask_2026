FROM python:3.14
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd -m -u 1000 appuser
USER appuser
EXPOSE 5000
#CMD ["flask", "--app", "app.py", "run", "--debug", "--host=0.0.0.0"]
CMD ["flask", "--app", "run.py", "run", "--debug", "--host=0.0.0.0"]
