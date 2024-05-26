FROM python:3.10.14

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

copy . .

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]



