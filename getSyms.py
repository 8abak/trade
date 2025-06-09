# File: getSyms.py

import json
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ctrader_open_api.client import Client

# Load credentials from file
creds_path = os.path.join(os.path.dirname(__file__), "credentials/creds.json")
with open(creds_path, "r") as f:
    creds = json.load(f)

# Initialize the client for live trading data
client = Client(
    host="live.ctraderapi.com",
    port=5036,
    protocol="protobuf"
)

# Handle and save the symbol list
def handle_symbol_list(message):
    symbols = message.payload.symbol
    print(f"Received {len(symbols)} symbols.")
    all_symbols = [{
        "symbolId": symbol.symbolId,
        "symbolName": symbol.symbolName,
        "description": symbol.description
    } for symbol in symbols]

    symbs_path = os.path.join(os.path.dirname(__file__), "credentials/symbs.json")
    with open(symbs_path, "w") as out:
        json.dump(all_symbols, out, indent=2)

    print("Saved all symbols to symbs.json")
    client.stop()

# Assign the handler and start client
client.on_symbol_list = handle_symbol_list
print("Connecting to cTrader live API and requesting symbols...")
client.start()
client.send_symbol_list_request(
    ctid_trader_account_id=creds["accountId"],
    access_token=creds["accessToken"],
    client_id=creds["clientId"],
    client_secret=creds["clientSecret"]
)
