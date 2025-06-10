import json
import os
import sys
from twisted.internet import reactor
from client import Client
from factory import Factory
from tcpProtocol import TcpProtocol
from OpenApiMessages_pb2 import ProtoOASubscribeSpotsReq
from OpenApiModelMessages_pb2 import ProtoOAPayloadType

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

# Message dispatcher
def messageRouter(_, message):
    if message.payloadType == ProtoOAPayloadType.PROTO_OA_SPOT_EVENT:
        handleTick(message)

# Create protocol
protocol = TcpProtocol()

# Init client
client = Client(
    host="live.ctraderapi.com",
    port=5035,
    protocol=protocol
)

client.setMessageReceivedCallback(messageRouter)

# On connection ready
def start():
    print("🔐 Connected. Subscribing to tick data...")

    req = ProtoOASubscribeSpotsReq()
    req.ctidTraderAccountId = creds["accountId"]
    req.symbolId.append(creds["symbolId"])

    client.send(req)

client.setConnectedCallback(lambda _: start())

# Run
client.run()
reactor.run()
