#!/usr/bin/env python

from twisted.internet.protocol import ClientFactory

class Factory(ClientFactory):
    def __init__(self, protocolClass, client):
        super().__init__()
        self.protocolClass = protocolClass  # Save the class (like TcpProtocol)
        self.client = client
        self.numberOfMessagesToSendPerSecond = self.client.numberOfMessagesToSendPerSecond

    def buildProtocol(self, addr):
        proto = self.protocolClass()       # Instantiate protocol
        proto.factory = self               # Give it reference to factory
        return proto

    def connected(self, protocol):
        self.client._connected(protocol)

    def disconnected(self, reason):
        self.client._disconnected(reason)

    def received(self, message):
        self.client._received(message)
