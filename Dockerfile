FROM python:3

WORKDIR /

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "api.py" ]
# CMD [ "python", "test_flaskr.py" ]