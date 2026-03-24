FROM python:3.11-slim


WORKDIR /backend


COPY requirements.txt ./


RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8001

COPY ./ .


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

# CMD ["fastapi", "run", "app/main.py", "--port", "8000"]