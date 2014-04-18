from flask import Flask, redirect, url_for, session, request, render_template, jsonify
from flask_oauthlib.client import OAuth
import requests

import os
os.environ['DEBUG'] = '1' # To work with OAuth server without https

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

agiliq = oauth.remote_app(
    'agiliq',
    consumer_key='D7PBWxpkEb4lEc52sD6r2ilZPVEbyasOCQG6FiMb9DXlTYhGCH',
    consumer_secret='GsW3W4NJsV1d4gKbZuOq7M8yLMwlCGgBa7m5uhqLTmHd6UIENq',
    request_token_params={'scope': 'user:email'},
    base_url='http://join.agiliq.com',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='http://join.agiliq.com/oauth/access_token',
    authorize_url='http://join.agiliq.com/oauth/authorize',
)

@app.route('/')
def index():
    if session.get('agiliq_token'):
        return redirect(url_for('submit'))
    return redirect(url_for('login'))

@app.route('/login')
def login():
    if session.get('agiliq_token'):
        return redirect(url_for('submit'))
    return agiliq.authorize(callback = url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('agiliq_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
@agiliq.authorized_handler
def authorized(resp):
    code = request.args.get('code')
    error = request.args.get('error')
    error_desc = request.args.get('error_description')
    if error:
    	return "Error occured : {} - {}".format(error,error_desc)

    params = { 
        "client_id":agiliq.consumer_key, 
        "client_secret":agiliq.consumer_secret, 
        "code":code, 
        "redirect_uri" : "http://local.dev.com:5000/login/authorized" 
        }
    r = requests.get(agiliq.access_token_url, params=params)

    data = r.json()

    session['agiliq_token'] = data['access_token']
    return redirect(url_for('submit'))

@app.route('/submit', methods = ['GET','POST'])
def submit():
	access_token = session.get('agiliq_token')
	if access_token:
		return render_template('submit.html', access_token = access_token)
	return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()