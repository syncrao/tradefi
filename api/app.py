from flask import Flask , render_template, request, jsonify
import pyotp, json, http.client, os, threading, time, sqlite3
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



def five_min(header, token, exc):

    date_str = datetime.now() 
    fdate_str = datetime.now() - timedelta(days=7)
    time_str = datetime.strptime("20:30", "%H:%M")
    date_str = date_str.strftime("%Y-%m-%d")
    time_str = time_str.strftime("%H:%M")
    fdate_str = fdate_str.strftime("%Y-%m-%d")
    payload = {
        "exchange": exc,
        "symboltoken": token,
        "interval": "ONE_DAY",
        "fromdate":  fdate_str+' 09:15',
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



def check_result(cdl , op , candle):
    if op == 101:
        if cdl < candle:
            return True
        else:
            return False
    elif op == 99:
        if cdl > candle:
            return True
        else:
            return False
    else:
        return "No Value"


def chek(candle, list):
    if len(candle) > len(list) and len(candle) > 4:
        for data in list:
            result = check_result(candle[data[0]][data[1]], data[2], candle[data[3]][data[4]])
            if not result:
                return False
        return True
    else:
        return False

def back(list):
    connc = sqlite3.connect('fiveMinCandle.db') 
    cursor = connc.cursor()
    cursor.execute('SELECT * FROM candles')
    rows = cursor.fetchall()
    result_list = []
    for row in rows:
        id, date, candle = row
        data_list = []
        data = json.loads(candle)
        entry = ""
        for candle in data:
            data_list.append(candle)
            if entry == "":
                result = chek(data_list, list)
                if result: 
                    entry = candle[4]
                else:
                    continue
            else:
                if candle[4] >  entry + 20:
                    
                    result_list.append(f"Date  : {date} - Entry Price : {entry} -  Exit Price: {candle[4]} - Book Profit {candle[4] - entry}")
                    entry = ""
                elif candle[4] <  entry - 10:
                    result_list.append(f"Date  : {date} - Entry Price : {entry} -  Exit Price: {candle[4]} - Book Loss {candle[4] - entry}")
                    entry = ""
                elif len(data_list) > 71:
                    result_list.append(f"Date  : {date} - Entry Price : {entry} -  Exit Price: {candle[4]} - Market Close {candle[4] - entry}")
                    entry = ""
                else:
                    continue
    return result_list


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/backtest')
def backtest():
    return render_template("backtest.html")


@app.route('/backdata', methods=['POST'])
def backdata():
    data = request.json
    list = [[int(item) for item in sublist] for sublist in data]
    print(list) 
    result_data = back(list)
    return jsonify({'status': 'success', 'data': result_data})



@app.route('/get_candle_data/<token>/<name>', methods=['GET'])
def get_candle_data(token, name):
    print(name)
    try:
        candle_data = five_min(headers, token, "NSE")
        return jsonify({"data": candle_data})
    
    except json.decoder.JSONDecodeError:
        return jsonify({"error": f"Error occurred while processing token: {token}"})

@app.route('/fut')
def fut():
    return render_template("fut.html")

@app.route('/get_fut_data/<token>/<name>', methods=['GET'])
def get_fut_data(token, name):
    try:
        candle_data = five_min(headers, token, "NFO")
        return jsonify({"data": candle_data})
    except json.decoder.JSONDecodeError:
        return jsonify({"error": f"Error occurred while processing token: {token}"})




if __name__ == '__main__':
    app.run(debug=True) 