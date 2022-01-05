FROM python:3

WORKDIR /app

COPY requirements.txt ./

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

COPY . .

ENV PORT=8080

EXPOSE 8080

CMD ["python", "bot.py"]