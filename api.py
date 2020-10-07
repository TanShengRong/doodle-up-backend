# from flask import Flask, flash, redirect, url_for
from flask_cors import CORS
import flask
from flask import request
from db import FirebaseHelper
from werkzeug.utils import secure_filename
import os


app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = './images'

helper = FirebaseHelper()

# upload from react js to flask
UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = {'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# upload progress(BLOB OR FILE?) to storage
# TODO: append storage link within realtime database w/ id
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return helper.upload_file(filepath, 'assets/')

# USER ENDPOINTS
# creates user in firebase authentication
# add username as displayName in userInfo
# creates entry in realtime database
# requires form
@app.route('/signup', methods=['POST'])
def sign_up():
    email = request.form['email']
    password = request.form['password']
    username = request.form['username']
    success = helper.create_new_user(email, password, username)
    if success:
        # initialize stories for user
        results = helper.get_all_content()

        for result in results:
            helper.start_new_story(username, result["id"])
    return success

# able to return a string:token that expires in 60minutes - potentially good for prototyping secure access
# returns username
# requires form
@app.route('/signin', methods=['POST'])
def sign_in():
    email = request.form['email']
    password = request.form['password']
    try:
        user_json = helper.sign_in_with_email_and_password(email, password)
        return user_json["displayName"], 200
    except Exception:
        return "Account does not exist or wrong credentials.", 400


# resets password by sending an email with a link
# e.g. /resetpassword?email=tsr@gmail.com
@app.route('/resetpassword', methods=['GET'])
def reset_password():
    email = request.args.get("email")
    returned_json = helper.send_password_reset_email(email)
    if "email" not in returned_json:
        return "Please re-enter your email", 400
    return "Sucessful! Please check your email", 200

# potentially checks token issue time, email
@app.route('/accountinfo/<string:idToken>', methods=['GET'])
def account_info(idToken):
    returned_json = helper.get_account_info(idToken)
    if "users" not in returned_json:
        return "Invalid token", 400
    return "Successful.", 200

# GAME PROGRESSION ENDPOINTS

# Save progress
# {
#     "story_id": myid,
#     "username": "popo",
#     "new_image": file,
#     "stage_id": 1.1,
#     "completed": True
# }
@app.route('/progress', methods=['POST'])
def save_user_progress():
    username = request.form['username']
    storyid = request.form['story_id']
    stage_id = request.form['stage_id']
    completed = request.form['completed']
    # json = request.get_json()
    # TODO: Saving file needs testing
    # file = json["new_image"]
    file = request.files['new_image']
    # file = request.form['new_image']
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        url = helper.upload_file(filepath, 'Progress/')
        os.remove(filepath)
    result = helper.update_story_progress(
        username, storyid, stage_id, url, completed)
    return result

# Get user's progress for the selected story, else initialize
# Important to note, storyid cannot me an integer string i.e. "1", "23"
# Firebase is sensitive and convert the data structure into an array
# /progress?username=xyz&storyid=1
@app.route('/progress', methods=['GET'])
def get_user_progress():
    username = request.args.get('username')
    storyid = request.args.get('storyid')
    progress = helper.get_story_progress(username, storyid)
    if not progress:
        progress = helper.start_new_story(username, storyid)
    return progress

# STORY CONTENT ENDPOINTS
# /content?storyid=001
@app.route('/content', methods=['GET'])
def get_content():
    storyid = request.args.get('storyid')
    content = helper.get_content(storyid)
    if not content:
        content = "Story content not found.", 400
    return content


@app.route('/content', methods=['POST'])
def create_content():
    # needs the request content to be set to application/json
    content = request.get_json()
    helper.create_content(content)
    return "Content created.", 200


@app.route('/content/all', methods=['GET'])
def get_all_content():
    contents = helper.get_all_content()
    if contents:
        return {"results": contents}
    else:
        return "Error", 400

@app.route('/')
def index():
    return 'Working'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
