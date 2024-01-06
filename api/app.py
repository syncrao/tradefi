from flask import Flask , render_template

import pyotp, json, http.client, os, threading, time
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = "srr"

load_dotenv()

api = os.getenv("api_key")

def main_login():
    global headers, jwt_token
    conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
    payload = {
                "clientcode": "S502639",
                "password": "9696",
                "totp": pyotp.TOTP("SWM6LBJHPTZ6YL5RHIN6JE7OSU").now()
            }
    api = "qATshT3J"
    payload_str = json.dumps(payload)
    headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
            'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
            'X-MACAddress': 'MAC_ADDRESS',
            'X-PrivateKey': api
        }

    conn.request("POST", "/rest/auth/angelbroking/user/v1/loginByPassword", payload_str, headers)
    res = conn.getresponse()
    data = res.read()
    response_json = json.loads(data.decode("utf-8"))
    jwt_token = response_json['data']['jwtToken']
    conn.close()
    headers = {
        'Authorization': 'Bearer '+jwt_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-UserType': 'USER',
        'X-SourceID': 'WEB',
        'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
        'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
        'X-MACAddress': 'MAC_ADDRESS',
        'X-PrivateKey': api
        }
    return headers, jwt_token, api


headers, jwt_token, api =  main_login()

counter = 0
def count():
    global counter
    while True:
        counter = counter + 1
        time.sleep(1)
        print(counter)



@app.route('/')
def index():
    count_thread = threading.Thread(target=count)
    count_thread.start()
    return render_template("index.html", counter=counter)

@app.route('/get_counter')
def get_counter():
    return str(counter)



if __name__ == '__main__':
    app.run(debug=True) 