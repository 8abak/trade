import os
import json
from twisted.internet import reactor
from ctrader_open_api.client import Client
from ctrader_open_api.messages.OpenApiMessages_pb2 import (
    ProtoOASubscribeSpotsReq,
    ProtoOASpotEvent,
)

# Load credentials
credsPath = os.path.join(os.path.dirname(__file__), "credentials/creds.json")
with open(credsPath, "r") as f:
    creds = json.load(f)

# Hardcoded symbol ID for XAUUSD (Gold)
goldSymbolId = 41

def onTick(message):
    quote = message.payload
    print(
        f"[Tick] Bid: {quote.bid}, Ask: {quote.ask}, Timestamp: {quote.timestamp}"
    )

def onConnected(client):
    print("✅ Connected")
    client.registerCustomHandler(ProtoOASpotEvent().payloadType, onTick)

    quoteReq = ProtoOASubscribeSpotsReq(
        ctidTraderAccountId=creds["ctidTraderAccountId"],
        symbolId=goldSymbolId,
    )
    client.send(ProtoOASubscribeSpotsReq().payloadType, quoteReq)

client = Client(
    clientId=creds["clientId"],
    clientSecret=creds["clientSecret"],
    accessToken=creds["accessToken"],
    ctidTraderAccountId=creds["ctidTraderAccountId"],
    onConnect=onConnected
)

client.connect()
reactor.run()
