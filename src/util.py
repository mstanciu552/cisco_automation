import os
import yaml
import argparse
import base64

def format_bash(str):
    return base64.b64encode(bytes(str, 'utf-8')).decode('utf-8')

def load_config(path: str):
    if not path:
        path = "./vars.yml"
    if not os.path.isfile(path):
        print("Config file required")
        exit(1)

    with open(os.path.expanduser(path), 'r') as file:
        return yaml.safe_load(file)
    

def format_html(str: str):
    return str.replace("\n", "<br />\n")

def format_newline(arr) -> str:
    return arr.split("\n")

def convert_to_list(arr) -> str:
    return "\n".join(arr)

def check_env(var, err) -> str:
    if not var:
        print(err)
        exit(1)

    return var

def handle_aruments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config')

    return parser.parse_args()

def format_ipv4_config(ipv4):
    if not "," in ipv4:
        return [ipv4]
    return ipv4.split(",")

def format_ipv4(ipv4):
    if "," in ipv4:
        return ipv4.split(",")

    if ":" in ipv4:
        pass

    return ipv4

def init(ipv4, username, password):
    ipv4 = format_ipv4_config(ipv4)
    content = f"""
    [devices]
    {convert_to_list(ipv4)}

    [devices:vars]
    ansible_user={username}
    ansible_password={password}
    ansible_connection=network_cli
    ansible_network_os=ios
    ansible_port=22
    """

    with open("./hosts.ini", "w") as hosts_file:
        hosts_file.write(content)
