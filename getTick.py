import json
import sys
import os
from twisted.internet import reactor
from client import Client
from factory import Factory
from tcpProtocol import TcpProtocol
from OpenApiMessages_pb2 import ProtoOAQuoteReq, ProtoOAPayloadType

# Ensure local directory is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Load credentials from local creds.json
with open("creds.json", "r") as f:
    creds = json.load(f)

# Handle incoming tick
def handleQuote(message):
    print("✅ Tick received:")
    print(message)
    client.stop()
    reactor.stop()

# Create protocol
protocol = TcpProtocol()

# Create and start client
client = Client(
    host="live.ctraderapi.com",
    port=5035,
    protocol=protocol
)

# Attach event handler
client.on(ProtoOAPayloadType.PROTO_OA_QUOTE_RES, handleQuote)

# Once client is ready, send quote request
def start():
    print("🔐 Authenticated. Requesting tick...")
    req = Factory.createQuoteRequest(
        accountId=creds["accountId"],
        symbolId=creds["symbolId"]
    )
    client.send(req)

client.onReady = start

# Start client and reactor
client.run()
reactor.run()
