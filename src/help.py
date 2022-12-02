def print_help():
    print(
        """
    In order to use this tool, you need to set some configuration values.
    All configuration will be done in the files: \n\t- vars.yml \n\t- hosts.ini\n\n

    In vars.yml you have to set the following:
    \t- tftp_server - server where you can get configuration files
    \t- ansible_receiver - email address you want to receive notification emails on
    \t- ansible_sender - email address of email sender (can be receiver)
    \t- ansible_gmail_user - username of the gmail account used to send data
    \t- ansible_gmail_password - password generated from a gmail account(not account password)
    \t- mail_subject - subject of mails to be sent
    \t- ipv4 - vector of IPs to be checked
    \t- base_path - path on controller system to a folder that stores configurations
    \t- baseline_switch_path - filename of switch baseline configuration on tftp server
    \t- baseline_router_path - filename of router baseline configuration on tftp server
    \n\n
    In hosts.ini you have to make a basic Ansible configuration for working with networking devices.
    """
    )
