from fuse_protocol import Client, create_default_logger

logger = create_default_logger()
c = Client("vim plugin", logger)
