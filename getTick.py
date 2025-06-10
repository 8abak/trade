import json
import os
import sys
from twisted.internet import reactor
from client import Client
from factory import Factory
from tcpProtocol import TcpProtocol
from OpenApiMessages_pb2 import ProtoOASubscribeSpotsReq, ProtoOAPayloadType

# Fix local imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Load credentials
with open("creds.json", "r") as f:
    creds = json.load(f)

# Tick response handler
def handleTick(message):
    print("✅ Tick received:")
    print(message)
    client.stop()
    reactor.stop()

# Create protocol
protocol = TcpProtocol()

# Init client
client = Client(
    host="live.ctraderapi.com",
    port=5035,
    protocol=protocol
)

# Bind handler
client.on(ProtoOAPayloadType.PROTO_OA_SPOT_EVENT, handleTick)

# On connection ready
def start():
    print("🔐 Connected. Subscribing to tick data...")

    req = ProtoOASubscribeSpotsReq()
    req.ctidTraderAccountId = creds["accountId"]
    req.symbolId.append(creds["symbolId"])

    client.send(req)

client.onReady = start

# Run
client.run()
reactor.run()
