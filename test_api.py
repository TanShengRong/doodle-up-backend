import requests
from api import app as flask_app
import pytest

@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client):
    res = client.get('/')
    assert res.status_code == 200
    expected = """
<pre>
 ######                                     #     #           ######                                            
 #     #  ####   ####  #####  #      ###### #     # #####     #     #   ##    ####  #    # ###### #    # #####  
 #     # #    # #    # #    # #      #      #     # #    #    #     #  #  #  #    # #   #  #      ##   # #    # 
 #     # #    # #    # #    # #      #####  #     # #    #    ######  #    # #      ####   #####  # #  # #    # 
 #     # #    # #    # #    # #      #      #     # #####     #     # ###### #      #  #   #      #  # # #    # 
 #     # #    # #    # #    # #      #      #     # #         #     # #    # #    # #   #  #      #   ## #    # 
 ######   ####   ####  #####  ###### ######  #####  #         ######  #    #  ####  #    # ###### #    # #####     
 </pre> 
"""
    assert expected == res.get_data(as_text=True)

def test_sign_in(client):
    payload = {'password': '123456',
    'email': 'pytest@gmail.com'}

    response = client.post(
        '/signin', 
        data = payload, 
        follow_redirects = True
    )
    assert response.status_code == 200
    assert b'pytest' in response.data

def test_sign_up(client):
    payload = {'username': 'pytest',
    'password': '123456',
    'email': 'pytest@gmail.com'}

    response = client.post(
        '/signup',
        data = payload,
        follow_redirects = True
    )
    # account already created, should return "The email is already in use", 400
    assert response.status_code == 400
    assert b'The email is already in use' in response.data