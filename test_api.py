import api
import os
import tempfile
import pytest

@pytest.fixture
def client():
    api.app.config['TESTING'] = True
    # api.app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))

    with api.app.test_client() as client:
        with api.app.app_context():
            # flaskr.init_db()
            api.app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
        yield client

    # os.close(db_fd)
    # os.unlink(flaskr.app.config['DATABASE'])

def test_progress(client):
    """Start with a blank database."""
    rv = client.get('/progress?username=jack&storyid=001')
    assert rv.data
    # rv = client.get('/')
    # assert b'No entries here so far' in rv.data