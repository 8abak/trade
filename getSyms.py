# File: getSyms.py

import json
import os
import sys
from twisted.internet import reactor

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ctrader_open_api.client import ClientService
from ctrader_open_api.client import Client
from ctrader_open_api.factory import Factory

# `ProtoOASymbolsListReq` is the protobuf message used to fetch all symbols.
# Importing the non-existent singular form would raise an ImportError.
from ctrader_open_api.messages.OpenApiMessages_pb2 import ProtoOASymbolsListReq

# Load credentials from file
creds_path = os.path.join(os.path.dirname(__file__), "credentials/creds.json")
with open(creds_path, "r") as f:
    creds = json.load(f)

# Handler for incoming symbol list
def handle_symbol_list(message):
    if not hasattr(message.payload, 'symbol'):
        print("No symbols found in response.")
        client_service.stop()
        reactor.stop()
        return

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
    client_service.stop()
    reactor.stop()

# Set up client and service
client = Client(
    host="live.ctraderapi.com",
    port=5036,
    protocol="protobuf"
)
client.on_symbol_list = handle_symbol_list

factory = Factory(client=client)
client_service = ClientService(client=client, factory=factory)

print("Connecting to cTrader live API and requesting symbols...")
client_service.startService(
    client_id=creds["clientId"],
    client_secret=creds["clientSecret"],
    access_token=creds["accessToken"]
)

symbol_list_request = ProtoOASymbolsListReq(
    ctidTraderAccountId=creds["accountId"]
)
client.send(symbol_list_request)

reactor.run()
