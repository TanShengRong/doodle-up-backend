import requests
from api import app as flask_app
import pytest
import io


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()

def test_index_get(client):
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

def test_sign_in_post(client):
    payload = {'password': '123456',
    'email': 'pytest@gmail.com'}

    response = client.post(
        '/signin', 
        data = payload, 
        follow_redirects = True
    )
    assert response.status_code == 200
    assert b'pytest' in response.data

def test_sign_up_post(client):
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

def test_progress_post(client):
    payload = {'username': 'pytest',
    'story_id': '001',
    'stage_id': '1',
    'completed': 'false'}

    response = client.post(
        '/progress',
        data = payload,
        follow_redirects = True
    )
    assert response.status_code == 200

def test_progress_get(client):
    response = client.get('/progress?username=pytest&storyid=001')
    assert response.status_code == 200

def test_reset_progress_post(client):
    payload = {'username': 'pytest',
    'story_id': '001'}

    response = client.post(
        '/reset',
        data = payload,
        follow_redirects = True
    )
    assert response.status_code == 200
    assert b'Reset Complete.' in response.data

def test_story_content_endpoint_get(client):
    response = client.get('/content?storyid=001')
    assert response.status_code == 200

def test_all_story_content_endpoint_get(client):
    response = client.get('/content?storyid=001')
    assert response.status_code != 400

def test_upload_post(client):
    payload = dict(
        file = (open('./images/question.png', 'rb'), 'question.png')
    )

    response = client.post(
        '/upload',
        data = payload,
        follow_redirects = True
    )
    assert response.status_code == 200