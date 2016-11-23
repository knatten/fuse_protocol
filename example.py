from fuse_protocol import Client, create_default_logger
import time

logger = create_default_logger()
def receive(msg):
    print msg


client = Client("vim plugin", logger)
client.add_receiver(receive)
client.send("Request", '{"Name":"Subscribe","Id":101,"Arguments":{"Filter":"Fuse.BuildLogged","Replay":false,"SubscriptionId":42}}')

raw_input("Press enter to exit...")
