from flask import Flask, render_template, url_for, request
from datetime import datetime
from twitter_map import location_map
# from requests import request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/map', methods=["POST"])
def map():
    token = request.form.get('bearer_token')
    username = request.form.get('username')
    location_map(username, token)
    return render_template('followers_locations.html')


if __name__ == '__main__':
    app.run(debug=True)