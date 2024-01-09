from flask import Flask , render_template, jsonify
import pyotp, json, http.client, os, threading, time
from datetime import datetime, timedelta
from dotenv import load_dotenv


app = Flask(__name__)
app.secret_key = "srr"

load_dotenv()

api = os.getenv("api_key")
conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

def main_login():
    global headers, jwt_token, api
    payload = {
                "clientcode": "S502639",
                "password": "9696",
                "totp": pyotp.TOTP("SWM6LBJHPTZ6YL5RHIN6JE7OSU").now()
            }
   
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


def five_min(header, token):

    date_str = datetime.now() 
    time_str = datetime.strptime("20:30", "%H:%M")
    date_str = date_str.strftime("%Y-%m-%d")
    time_str = time_str.strftime("%H:%M")
    payload = {
        "exchange": "NSE",
        "symboltoken": token,
        "interval": "ONE_DAY",
        "fromdate":  '2024-01-02 09:15',
        "todate": date_str+' '+time_str
    }
    payload_str = json.dumps(payload)

    conn.request("POST", "/rest/secure/angelbroking/historical/v1/getCandleData", payload_str, header)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    conn.close()
    data_dict = json.loads(data)
    candle_data = data_dict['data']
    return candle_data



@app.route('/')
def index():
    return render_template("index.html")


@app.route('/get_candle_data/<token>', methods=['GET'])
def get_candle_data(token):
    try:
        candle_data = five_min(headers, token)
        return jsonify({"data": candle_data})
    except json.decoder.JSONDecodeError:
        return jsonify({"error": f"Error occurred while processing token: {token}"})


if __name__ == '__main__':
    app.run(debug=True) 