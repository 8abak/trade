import json
from ctrader_open_api.client import Client

with open("../credentials/creds.json", "r") as f:
    creds = json.load(f)

client=Client(
    clientId=creds["clientId"],
    clientSecret=creds["clientSecret"],
    accessToken=creds["accessToken"]
)

def handle_symbol_list(message):
    symbols = message.payload.symbol
    print(f"received {len(symbols)} symbols.")
    all_symbols=[{
        "symbolId": s.symbold,
        "symbolName": s.symbolName,
        "description": s.description
    } for s in symbols] 

    with open("../credentials/syms.json", "w") as out:
        json.dump(all_symbols, out, indent=2)
    print("Saved all symbols to syms.json")
    client.stop()

client.on_symbol_list=handle_symbol_list

print("Connecting and requesting symbols...")

client.start()
client.send_symbol_list_request(ctid_trader_account_id=creds["accountId"])
