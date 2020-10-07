FROM python:3.8-slim-buster

WORKDIR /

COPY requirements.txt ./
# RUN pip3 install --upgrade setuptools
# RUN pip3 install --upgrade gcloud
# RUN pip3 install --upgrade pycryptodome
# RUN pip3 install --upgrade requests_toolbelt
# RUN pip3 install --upgrade python-jwt
# RUN pip3 install --upgrade requests
# RUN pip3 install --upgrade oauth2client
# RUN pip3 install --upgrade jws
# RUN pip3 install --upgrade pyrebase
RUN pip install --upgrade pip
RUN python -m pip install pyrebase
# RUN pip install -r requirements.txt

COPY . .

# EXPOSE 5000

CMD [ "python", "api.py" ]
# CMD [ "python", "test_flaskr.py" ]