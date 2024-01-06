import pyotp, json, http.client

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