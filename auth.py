import os, json
from dotenv import load_dotenv
from requests import get, post
from webbrowser import open
import math, random, re
import base64


# Function to generate state value
def gen_state(size : int) -> str:
    state = ''
    possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    for _ in range(size):
        state += possible[math.floor(random.random() * len(possible))]
    return state

class Auth:
    def __init__(self, client_id : str, secret : str, response_type : str, redirect_uri : str, scope : str):
        # Get client credentials and header requirements
        self.id = client_id
        self.secret = secret
        self.response_type = response_type
        self.redirect_uri = redirect_uri
        self.state = gen_state(16)
        self.scope = scope
        self.auth_code = self.get_auth_code()
        self.access_token = self.get_access_token(self.auth_code)

    # Get user authorization code to be given playlist editing rights
    def get_auth_code(self) -> str:
        auth_url = 'https://accounts.spotify.com/authorize?'
        redirect_url = f'{auth_url}&client_id={self.id}&response_type={self.response_type}&redirect_uri={self.redirect_uri}&state={self.state}&scope={self.scope}'
        open(redirect_url)
        
        auth_code_url = input("Enter redirect URL: ")

        match = re.search(r'code=([^&]+)', auth_code_url)
        try:
            return match.group(1)
        except:
            raise ValueError()
        
    # Get access token 
    def get_access_token(self, auth_code : str) -> str:
        auth_bytes = f'{self.id}:{self.secret}'.encode('utf-8')
        headers = {
            'Authorization':'Basic ' + str(base64.b64encode(auth_bytes), 'utf-8'),
            'Content-Type':'application/x-www-form-urlencoded'
        }

        data = {
            'grant_type':'authorization_code',
            'code':auth_code,
            'redirect_uri':self.redirect_uri
        }

        api_url = 'https://accounts.spotify.com/api/token'
        response = post(api_url, headers=headers, data=data)

        response_json = json.loads(response.content)

        access_token = response_json['access_token']
        return access_token
    
    def get_auth_header(self) -> json:
        auth_bytes = f'{self.id}:{self.secret}'.encode('utf-8')
        header = {
            'Authorization':'Bearer ' + self.access_token,
            'Content-Type':'application/json'   
        }

        return header








