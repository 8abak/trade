# File: scripts/getSyms.py

import json
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ctrader_open_api.client import Client

creds_path = os.path.join(os.path.dirname(__file__), "../credentials/creds.json")
with open(os.path.abspath(creds_path), "r") as f:
    creds = json.load(f)

client = Client()


def handle_symbol_list(message):
    symbols = message.payload.symbol
    print(f"Received {len(symbols)} symbols.")
    all_symbols = [{
        "symbolId": symbol.symbolId,
        "symbolName": symbol.symbolName,
        "description": symbol.description
    } for symbol in symbols]

    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "../credentials/symbs.json")), "w") as out:
        json.dump(all_symbols, out, indent=2)
    print("Saved all symbols to symbs.json")
    client.stop()

client.on_symbol_list = handle_symbol_list
print("Connecting and requesting symbols...")
client.start()
client.send_symbol_list_request(ctid_trader_account_id=creds["accountId"])
