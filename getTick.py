import json
from twisted.internet import reactor
from ctrader_open_api.client import Client
from ctrader_open_api.factory import Factory
from ctrader_open_api.messages.OpenApiMessages_pb2 import ProtoOAPayloadType

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
