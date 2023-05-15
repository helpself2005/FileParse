FROM sanmaomashi/python:3.7.13-ubuntu18.04-paddle2.4.2

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1701"]