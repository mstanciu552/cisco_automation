import os
import tftpy
from enum import Enum
from diff import get_diff
from base64 import b64decode
from util import handle_aruments, isBase64, load_config


class ConfigType(Enum):
    IDEAL = 1
    STARTUP = 2
    RUNNING = 3

    def __str__(self):
        return self.name


class Config:
    ip: str
    text: str
    type: ConfigType

    def __init__(self, ip: str, type: ConfigType, text=None):
        self.type = type
        self.ip = ip

        args = handle_aruments()
        config = load_config(args.config)

        if not text:
            self.text = ""
        if not isBase64(text):
            self.text = str(text)
        else:
            self.text = b64decode(str(text)).decode("ascii")
        if type == ConfigType.IDEAL:
            self.get_tftp(
                config["tftp_server"],
                config["ideal_switch_path"],
                f"{config['base_path']}/{self.type}/{self.ip}.ios",
            )
        else:
            self.read_path(f"{config['base_path']}/{self.type}/{self.ip}.ios")

    def read_path(self, path):
        with open(os.path.expanduser(path)) as config:
            self.text = config.read()

    def compareWith(self, other):
        differences = get_diff(self.text, other.text)
        return differences

    def get_tftp(self, ip: str, path: str, dest: str):
        if not os.path.exists(os.path.basename(dest)):
            os.makedirs(os.path.basename(dest))
        client = tftpy.TftpClient(host=ip)
        client.download(path, dest)

        with open(os.path.expanduser(dest)) as config:
            self.text = config.read()

    def __str__(self):
        return self.text
