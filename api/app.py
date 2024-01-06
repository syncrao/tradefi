from flask import Flask 
import pyotp, json, http.client
from appfunction import main_login

app = Flask(__name__)
app.secret_key = "srr"
headers, jwt_token, api =  main_login()

@app.route('/')
def index():
    return headers





if __name__ == '__main__':
    app.run(debug=True) 