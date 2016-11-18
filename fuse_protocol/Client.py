import os
import logging
import logging.handlers
import subprocess

from threading import Thread

class Client:
    def __init__(self, name, receive, logger = None):
        self.name = name
        self.receive = receive
        self._configure_logging(logger)
        self._check_for_fuse()
        self._start()

    def send(self, msg_type, msg):
        self.process.stdin.write(self._format(msg_type, msg))

    def _configure_logging(self, logger):
        if logger is None:
            self.logger = logging.getLogger("null")
            self.logger.addHandler(logging.NullHandler)
            self.logger.setLevel(logging.CRITICAL)
        else:
            self.logger = logger
        self.logger.warning("Initialized client '{0}'".format(self.name))

    def _check_for_fuse(self):
        fuse_version= ["fuse", "--version"]
        self.logger.info("Checking for Fuse")
        try:
            p = subprocess.Popen(fuse_version, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            self.logger.info(stdout)
            if stderr:
                self.logger.error(stderr)
            if p.returncode != 0:
                msg = "Error checking for fuse. '" + " ".join(fuse_version) + "' returned '" + str(p.returncode)
                self.logger.error(msg)
                raise FuseError(msg)
        except OSError as e:
            msg = "Error checking for fuse, could not call '{0}'".format(" ".join(fuse_version))
            self.logger.error(msg)
            raise FuseNotFoundError(msg)
        
    def _format(self, msg_type, msg):
        return msg_type + "\n" + str(len(msg)) + "\n" + msg

    def _start(self):
        daemon_client = ["fuse", "daemon-client", self.name]
        try:
            self.process = subprocess.Popen(daemon_client, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            t = Thread(target=self._read_output, args=(self.process.stdout,))
            t.daemon = True
            t.start()
        except OSError as e:
            msg = "Error starting daemon-client, could not call '{0}'".format(" ".join(daemon_client))
            self.logger.error(msg)
            raise FuseNotFoundError(msg)

    def _read_output(self, stdout):
        for line in iter(stdout.readline, b''):
            self.receive(line)

class FuseNotFoundError(Exception):
    pass

class FuseError(Exception):
    pass

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
