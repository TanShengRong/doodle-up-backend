from flask import Flask, flash, redirect, url_for
import flask
from flask import jsonify, request, Response
from temp import stories
from db import FirebaseHelper
from werkzeug.utils import secure_filename
import os


app = flask.Flask(__name__)
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

# access storage for assets
# e.g. localhost:88888/asseturl?file_location=assets/car.png&token=123
@app.route('/asseturl', methods=['GET'])
def asset_url():
    file_location = request.args.get("file_location")
    token = request.args.get("token")
    return helper.get_asset_url(file_location, token)

# creates user in firebase authentication
# creates entry in realtime database
# requires form
@app.route('/signup', methods=['POST'])
def sign_up():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    if helper.get_user(username):
        return "The username has been taken.", 400
    helper.create_new_user(username, email, password)
    return "User created.", 200

# able to return a string:token that expires in 60minutes - potentially good for prototyping secure access
# requires form
@app.route('/signin', methods=['POST'])
def sign_in():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    if not helper.get_user(username):
        return "Does not exist, please create an account.", 400
    # return helper.sign_in_with_email_and_password(email, password)["idToken"]
    return "Account successfully logged in", 200

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
@app.route('/progress', methods=['POST'])
def save():
    username = request.args.get('username')
    storyid = request.args.get('storyid')
    json = request.get_json()
    # TODO: Saving file needs testing
    # file = json["new_image"]
    file = request.files['new_image']
    # file = request.form['new_image']
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        path = 'Progress/' + username
        url = helper.upload_file(path, filepath)
        json["content"]["image_url"] = url
        os.remove(filepath)
    helper.update_story_progress(username, storyid, json["content"])
    return "Progress saved", 200

# Get user's progress for the selected story, else initialize
# Important to note, storyid cannot me an integer string i.e. "1", "23"
# Firebase is sensitive and convert the data structure into an array
# /progress?username=xyz&story=1
@app.route('/progress', methods=['GET'])
def get_user_progress():
    username = request.args.get('username')
    storyid = request.args.get('storyid')
    progress = helper.get_story_progress(username, storyid)
    if not progress:
        progress = helper.start_new_story(username, storyid)
    return progress


@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    result = helper.get_user(username)
    if not result:
        result = Response({"error": "User not found."},
                          status=404, mimetype='application/json')
    return result

# STORY CONTENT ENDPOINTS
# /content?storyid=001
@app.route('/content', methods=['GET'])
def get_content():
    storyid = request.args.get('storyid')
    content = helper.get_content(storyid)
    if not content:
        content = Response({"error": "Story not found."},
                           status=404, mimetype='application/json')
    return content


@app.route('/content', methods=['POST'])
def create_content():
    # needs the request content to be set to application/json
    content = request.get_json()
    helper.create_content(content)
    return "Content created.", 200


if __name__ == "__main__":
    app.run()
