import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import json
from twisted.internet import reactor
from client import Client
from factory import Factory
import OpenApiCommonMessages_pb2
print(dir(OpenApiCommonMessages_pb2))

# Load credentials (same folder)
with open("creds.json", "r") as f:
    creds = json.load(f)

# Tick response handler
def handleQuote(message):
    print("✅ Tick received:")
    print(message)
    client.stop()
    reactor.stop()

# Init client
client = Client(
    host="live.ctraderapi.com",
    port=5035,
    clientId=creds["clientId"],
    clientSecret=creds["clientSecret"],
    accessToken=creds["accessToken"],
    ctidTraderAccountId=creds["accountId"]
)

client.on(ProtoOAPayloadType.PROTO_OA_QUOTE_RES, handleQuote)

def start():
    print("🔐 Authenticated. Subscribing to tick...")
    req = Factory.createQuoteRequest(creds["accountId"], creds["symbolId"])
    client.send(req)

client.onReady = start

# Start event loop
client.run()
reactor.run()
