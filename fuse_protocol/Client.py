import os
import logging
import logging.handlers
import subprocess

class Client:
    def __init__(self, name, logger = None):
        self.name = name
        self.configure_logging(logger)
        self.check_for_fuse()

    def configure_logging(self, logger):
        if logger is None:
            self.logger = logging.getLogger("null")
            self.logger.addHandler(logging.NullHandler)
            self.logger.setLevel(logging.CRITICAL)
        else:
            self.logger = logger
        self.logger.warning("Initialized client '{0}'".format(self.name))

    def check_for_fuse(self):
        fuse_version= ["fuse", "--version"]
        self.logger.info("Checking for Fuse")
        try:
            p = subprocess.Popen(fuse_version, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            self.logger.info(stdout)
            if stderr:
                self.logger.error(stderr)
            if p.returncode != 0:
                self.logger.error("Error checking for fuse. '" + " ".join(fuse_version) + "' returned '" + str(p.returncode))
        except OSError as e:
            self.logger.error("Error checking for fuse, could not call '{0}'".format(" ".join(fuse_version)))
        
def userdata_dir():
    if os.name == "posix":
        return os.path.join(os.getenv("HOME"), ".fuse")
    else:
        return os.path.join(os.getenv("LOCALAPPDATA"), "Fusetools", "Fuse")

def log_dir():
    return os.path.join(userdata_dir(), "logs")

def log_file():
    return os.path.join(log_dir(), "python-protocol.log")

def create_default_logger():
    logger = logging.getLogger("fuse-protocol")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)-15s %(message)s")
    handler = logging.handlers.RotatingFileHandler(log_file(), "a", 500000, 5, "utf-8")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
