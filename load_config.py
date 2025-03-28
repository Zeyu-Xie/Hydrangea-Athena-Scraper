import os
from datetime import datetime
import yaml

config_path = os.path.join(os.path.dirname(__file__), "config.yaml")


def load_config():
    with open(config_path, "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)


config = load_config()
FolderID = config["FolderID"]
DownloadPath = os.path.join(
    config["DownloadPath"], "Athena_" + datetime.now().strftime("%Y%m%d%H%M%S%f")
)
AutoLogin = config["AutoLogin"]
Username = config["Username"]
Password = config["Password"]
CommandLineLog = config["CommandLineLog"]
FileLog = config["FileLog"]
FileLogPath = os.path.join(DownloadPath, "log.txt")
DownloadLinkPage = config["DownloadLinkPage"]
DownloadGroupRegistrationPage = config["DownloadGroupRegistrationPage"]