#!/usr/bin/env python

from collections import deque
from twisted.protocols.basic import Int32StringReceiver
from twisted.internet import task
from OpenApiCommonMessages_pb2 import ProtoMessage, ProtoHeartbeatEvent
from protobuf import Protobuf


class TcpProtocol(Int32StringReceiver):
    MAX_LENGTH = 15000000
    _send_queue = deque()
    _send_task = None
    _lastSendMessageTime = None

    def connectionMade(self):
        super().connectionMade()
        self.factory.connected(self)  # 👈 This is crucial

        if not self._send_task:
            self._send_task = task.LoopingCall(self._sendStrings)
            self._send_task.start(1)

    def stringReceived(self, data):
        message = ProtoMessage()
        message.ParseFromString(data)
        self.factory.received(message)

    def send(self, message, clientMsgId=None, isCanceled=lambda: False):
        if isCanceled():
            return

        serialized = Protobuf.serialize(message, clientMsgId)
        self._send_que
