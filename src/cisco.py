import os
import tftpy
import subprocess
import difflib as dl
from util import convert_to_list, handle_aruments, load_config

TFTP_SERVER = load_config(handle_aruments().config)['tftp_server']

client = tftpy.TftpClient(TFTP_SERVER, 69)

def handler(running_config, ideal_config):
    differences = []
    for diff in dl.unified_diff(running_config.split("\n"), ideal_config.split("\n")):
        differences.append(diff)
    return differences

def run_ansible():
    subprocess.run(["ansible-playbook", "playbooks/get_startup.yml", "-i", "./hosts.ini"])
    subprocess.run(["ansible-playbook", "playbooks/get_running.yml", "-i", "./hosts.ini"])

def get_diff_ansible_ideal():
    subprocess.run(["ansible-playbook", "playbooks/get_startup.yml", "-i", "./hosts.ini"])

def get_diff_ideal_startup(ip):
    with open(
        os.path.expanduser(f"~/.ansible/show_output/startup_config/{ip}.ios"), "r"
    ) as file, open("/srv/tftp/lab_test/SW1.ios", "r") as ideal_config_file:
        startup_config = file.read()
        ideal_config = ideal_config_file.read()
        if not startup_config == ideal_config:
            return convert_to_list(handler(startup_config, ideal_config))
        else:
            return "Ideal configuration is the startup configuration"

def get_diff_ansible_startup():
    subprocess.run(["ansible-playbook", "playbooks/get_running.yml", "-i", "./hosts.ini"])
    subprocess.run(["ansible-playbook", "playbooks/get_startup.yml", "-i", "./hosts.ini"])

def get_diff_startup_running(ip):
    with open(
        os.path.expanduser(f"~/.ansible/show_output/running_config/{ip}.ios"), "r"
    ) as running, open(
        os.path.expanduser(f"~/.ansible/show_output/startup_config/{ip}.ios"), "r"
    ) as startup:
        running_config = running.read()
        startup_config = startup.read()
        if not running_config == startup_config:
            return convert_to_list(handler(running_config, startup_config))
        else:
            return "Ideal configuration is the running configuration"
