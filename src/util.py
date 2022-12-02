import os
import yaml
import argparse
import base64
import subprocess
import difflib as dl


def get_diff(config1, config2):
    differences = []
    for diff in dl.unified_diff(config1.split("\n"), config2.split("\n")):
        differences.append(diff)
    return "\n".join(differences)


def check_if_router(ip) -> bool:
    result = subprocess.run(
        "ansible-playbook -i hosts.ini playbooks/check_if_router.yml | grep -i failed=1 | awk '{print $1}'",
        stdout=subprocess.PIPE,
        shell=True,
    )
    switches = result.stdout.decode("utf-8").split("\n")[:-1]
    return ip not in switches


def run_ansible():
    subprocess.run(
        ["ansible-playbook", "playbooks/get_startup.yml", "-i", "./hosts.ini"]
    )
    subprocess.run(
        ["ansible-playbook", "playbooks/get_running.yml", "-i", "./hosts.ini"]
    )


def isBase64(sb):
    try:
        if isinstance(sb, str):
            # If there's any unicode here, an exception will be thrown and the function will return false
            sb_bytes = bytes(sb, "ascii")
        elif isinstance(sb, bytes):
            sb_bytes = sb
        else:
            raise ValueError("Argument must be string or bytes")
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except Exception:
        return False


def format_bash(str):
    return base64.b64encode(bytes(str, "utf-8")).decode("utf-8")


def load_config(path: str):
    if not path or path == "":
        path = "./vars.yml"
    if not os.path.isfile(path):
        print("Config file required")
        exit(1)

    with open(os.path.expanduser(path), "r") as file:
        config = yaml.safe_load(file)

        if not os.path.exists(config["base_path"]):
            os.makedirs(config["base_path"])

        return config


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
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("-c", "--config")
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("-d", "--daemon", action="store_true")

    return parser.parse_args()


def format_ipv4_config(ipv4):
    if not "," in ipv4:
        return [ipv4]
    return ipv4.split(",")


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
