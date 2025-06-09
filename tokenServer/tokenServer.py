from flask import Flask, request
import json
import requests
import os

app = Flask(__name__)
cred_path = os.path.join(os.path.dirname(__file__), '..', 'openApiClient', 'credentials.json')

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "❌ Missing authorization code", 400

    # Load credentials
    with open(cred_path) as f:
        creds = json.load(f)

    # Exchange code for access token
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': creds['redirect'],
        'client_id': creds['clientId'],
        'client_secret': creds['clientSecret']
    }

    response = requests.post('https://connect.spotware.com/apps/token', data=data)
    if response.status_code != 200:
        return f"❌ Token exchange failed: {response.text}", 500

    token_data = response.json()
    if 'accessToken' in token_data:
        creds['accessToken'] = token_data['accessToken']
    else:
        return f"❌ Token exchange failed: {token_data}", 500


    # Save updated credentials
    with open(cred_path, 'w') as f:
        json.dump(creds, f, indent=2)

    return "✅ Access token saved and written to credentials.json"

if __name__ == '__main__':
	app.run(
	    host='0.0.0.0',
	    port=443,
	    ssl_context=(
	        '/etc/letsencrypt/live/datavis.au/fullchain.pem',
	        '/etc/letsencrypt/live/datavis.au/privkey.pem'
	    )
	)
