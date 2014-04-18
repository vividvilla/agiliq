from flask import Flask, redirect, url_for, session, request, jsonify
import requests

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

consumer_key='9d54c63869a64a45474d'
consumer_secret='093870a219475fc587214fec6d3cc4e901c6ba94'
request_token_params={'scope': 'user:email'}
base_url='https://api.github.com/'
request_token_url=None
access_token_method='POST'
access_token_url='https://github.com/login/oauth/access_token'
authorize_url='https://github.com/login/oauth/authorize'

@app.route('/')
def index():
    if session.get('agiliq_token'):
        return redirect(url_for('submit'))
    return redirect(url_for('login'))

@app.route('/login')
def login():
    if session.get('agiliq_token'):
        return redirect(url_for('submit'))
    return redirect(authorize_url+resp+client+redi)
    # return type(resp)

@app.route('/logout')
def logout():
    session.pop('agiliq_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    code = request.args.get('code')
    # error = request.args.get('error')
    # error_desc = request.args.get('error_description')
    # if error:
    # 	return "Error occured : {} - {}".format(error,error_desc)

    # session['agiliq_token'] = code
    # return redirect(url_for('submit'))
    # if resp is None:
    #     return 'Access denied: reason=%s error=%s' % (
    #         request.args['error_reason'],
    #         request.args['error_description']
    #     )
    # session['agiliq_token'] = (resp['access_token'], '')
    # return str(resp.keys())
    return code
    
# @agiliq.tokengetter
# def get_agiliq_oauth_token():
#     return session.get('agiliq_token')

# @app.route('/submit', methods = ['GET','POST'])
# def submit():
# 	access_token = session.get('agiliq_token')
# 	if access_token:
# 		return render_template('submit.html', access_token = access_token)
# 	return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()