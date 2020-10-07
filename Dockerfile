FROM python:3.8-slim-buster

WORKDIR /

COPY requirements.txt ./
RUN pip3 install --upgrade setuptools
RUN pip3 install --upgrade gcloud
RUN pip3 install pyrebase
RUN pip install -r requirements.txt

COPY . .

# EXPOSE 5000

CMD [ "python", "api.py" ]
# CMD [ "python", "test_flaskr.py" ]