import json
from datetime import datetime, timedelta

symbols_list = [
    "ADANIPORTS-EQ", "ASIANPAINT-EQ", "AXISBANK-EQ", "BAJAJ-AUTO-EQ", "BAJFINANCE-EQ",
    "BAJAJFINSV-EQ", "BAJAJHLDNG-EQ", "BHARTIARTL-EQ", "BRITANNIA-EQ", "CIPLA-EQ",
    "COALINDIA-EQ", "DIVISLAB-EQ", "DRREDDY-EQ", "EICHERMOT-EQ", "GRASIM-EQ",
    "HCLTECH-EQ", "HDFCBANK-EQ", "HDFCLIFE-EQ", "HEROMOTOCO-EQ", "HINDALCO-EQ",
    "HINDUNILVR-EQ", "ICICIBANK-EQ", "INDUSINDBK-EQ", "INFY-EQ", "ITC-EQ",
    "JSWSTEEL-EQ", "KOTAKBANK-EQ", "LT-EQ", "M&M-EQ", "MARUTI-EQ",
    "NESTLEIND-EQ", "NTPC-EQ", "ONGC-EQ", "POWERGRID-EQ", "RELIANCE-EQ",
    "SHREECEM-EQ", "SBIN-EQ", "SBILIFE-EQ", "TATACONSUM-EQ", "TATAMOTORS-EQ",
    "TATASTEEL-EQ", "TCS-EQ", "TECHM-EQ", "TITAN-EQ", "ULTRACEMCO-EQ",
    "UPL-EQ", "WIPRO-EQ", "ADANIGREEN-EQ", "DIVISLAB-EQ", "JSWSTEEL-EQ"
]

def generate_month_year():
    today = datetime.now()
    current_month = today.strftime("%b%y").upper() 
    
    next_month = today + timedelta(days=5)
    next_month_str = next_month.strftime("%b%y").upper()
    
    return [current_month, next_month_str]

months_list = generate_month_year()

with open('data.json', 'r') as file:
    data = json.load(file)

symbol_token_dict = {}

for item in data:
    for name in symbols_list:
        for month in months_list:
            symbol = f"{month}FUT"
            if item['symbol'].endswith(symbol):
                symbol_token_dict[item['symbol']] = item['token']

with open('token.json', 'w') as file:
    json.dump(symbol_token_dict, file, indent=4)

print("Symbol-Token Pairs ending with 'FUT' saved in token_list.json")