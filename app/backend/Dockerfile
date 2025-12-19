FROM python:3.11


WORKDIR /backend


COPY requirements.txt ./


RUN pip install --no-cache-dir --upgrade -r requirements.txt


COPY ./backend /app/backend


CMD ["fastapi", "run", "app/main.py", "--port", "80"]