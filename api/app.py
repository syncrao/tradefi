from flask import Flask , render_template
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

symbol_token_dict = {
    "SHREECEM-EQ": "3103",
    "ADANIPORTS-EQ": "15083",
    "HDFCBANK-EQ": "1333",
    "TITAN-EQ": "3506",
    "TECHM-EQ": "13538",
    "COALINDIA-EQ": "20374",
    "INDUSINDBK-EQ": "5258",
    "M&M-EQ": "2031",
    "TATASTEEL-EQ": "3499",
    "HINDALCO-EQ": "1363",
    "AXISBANK-EQ": "5900",
    "GRASIM-EQ": "1232",
    "BAJFINANCE-EQ": "317"
    
}

symbol_token = {
    "BAJAJ-AUTO-EQ": "16669",
    "HINDUNILVR-EQ": "1394",
    "LT-EQ": "11483",
    "BRITANNIA-EQ": "547",
    "JSWSTEEL-EQ": "11723",
    "SBIN-EQ": "3045",
    "ICICIBANK-EQ": "4963",
    "POWERGRID-EQ": "14977",
    "HEROMOTOCO-EQ": "1348",
    "SBILIFE-EQ": "21808",
    "BAJAJHLDNG-EQ": "305",
    "ADANIGREEN-EQ": "3563",
    "BAJAJFINSV-EQ": "16675",
    "CIPLA-EQ": "694",
    "UPL-EQ": "11287",
    "ITC-EQ": "1660",
    "TATAMOTORS-EQ": "3456",
    "TATACONSUM-EQ": "3432",
    "BHARTIARTL-EQ": "10604",
    "WIPRO-EQ": "3787",
    "ULTRACEMCO-EQ": "11532",
    "HDFCLIFE-EQ": "467",
    "KOTAKBANK-EQ": "1922",
    "NTPC-EQ": "11630",
    "ONGC-EQ": "2475",
    "DIVISLAB-EQ": "10940",
    "TCS-EQ": "11536",
    "NESTLEIND-EQ": "17963",
    "DRREDDY-EQ": "881",
    "ASIANPAINT-EQ": "236",
    "RELIANCE-EQ": "2885",
    "EICHERMOT-EQ": "910",
    "MARUTI-EQ": "10999",
    "INFY-EQ": "1594",
    "HCLTECH-EQ": "7229"
}

@app.route('/')
def index():
    candle_data_list = []
    for symbol, token in symbol_token_dict.items():
        try:
            candle_data = five_min(headers, token)
            candle_data_list.append({"symbol": symbol, "data": candle_data})
        except json.decoder.JSONDecodeError:
            print(f"Error occurred while processing {symbol}")
            continue
    return render_template("index.html", candle_data_list=candle_data_list)




if __name__ == '__main__':
    app.run(debug=True) 