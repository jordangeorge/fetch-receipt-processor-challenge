FROM python:3

WORKDIR /code

ADD ./src .

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000

ADD start.sh .
RUN chmod +x start.sh
CMD ["./start.sh"]