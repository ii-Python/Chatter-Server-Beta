# Modules
import json
from os.path import exists

# Master function
def load_config():

    """Loads the config.json file into memory"""

    if not exists("config.json"):

        config = {
            "port": 7555,
            "host": "0.0.0.0",
            "code": None,
            "banned_ips": [],
            "admin_ips": []
        }

        with open("config.json", "w+") as f:
            
            f.write(json.dumps(config, indent = 4))

    try:

        with open("config.json", "r") as f:
            config = json.loads(f.read())

    except:

        raise SystemError("failed to read configuration file")

    return config
