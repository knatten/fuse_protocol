from fuse_protocol import FuseProtocol, create_default_logger
import time

logger = create_default_logger()
def receive(msg):
    print "RECV '" + msg + "'"

# class DaemonProtocol:
#     def __init__(self, fuse_protocol):
#         self.fuse_protocol = fuse_protocol
#         self._nextId = 0
#         self._nextSubscriptionId = 0
#         self._subscriptions = {}
#         self.fuse_protocol.add_receiver(self._receive)

#     def _receive(self, msg):
#         receive(msg)

#     def subscribe(self, eventType, handler):
#         requestId = self._nextId
#         subscriptionId = self._nextSubscriptionId
#         self._nextId += 1
#         self._nextSubscriptionId += 1
#         self._subscriptions[subscriptionId] = handler
#         self.fuse_protocol.send("Request",
#             '{"Name":"Subscribe","Id": ' + str(requestId) +
#             ',"Arguments":{"Filter":' + eventType  +
#             ',"Replay":false,"SubscriptionId": ' + str(subscriptionId) + '}}')
#         return subscriptionId

fuse_protocol = FuseProtocol("vim plugin", logger)
fuse_protocol.add_receiver(receive)
fuse_protocol.send("Request", '{"Name":"Subscribe","Id":101,"Arguments":{"Filter":"Fuse.BuildLogged","Replay":false,"SubscriptionId":42}}')

# def build_logged(msg):
#     print "Build Logged: '{0}'".format(msg)

# p.subscribe("Fuse.BuildLogged", build_logged)

raw_input("Press enter to exit...")
