FROM python:3

WORKDIR /

# COPY requirements.txt ./

# RUN pip3 install pyrebase
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

# EXPOSE 5000

CMD [ "python", "api.py" ]
# CMD [ "python", "test_flaskr.py" ]