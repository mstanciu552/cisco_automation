#!/home/mihai/cisco_automation/venv/bin/python
import sys
import time
import subprocess
from util import (
    format_html,
    handle_aruments,
    load_config,
    format_bash,
    run_ansible,
    get_diff,
)
from help import print_help
from Config import Config, ConfigType


def send_email(body):
    body = format_bash(body)
    subprocess.run(
        [
            "ansible-playbook",
            "playbooks/send_mail.yml",
            "-e",
            f"body64={body}",
        ]
    )


def main(args):
    config = load_config(args.config)

    if args.help:
        print_help()
        return

    run_ansible()
    html_text = """\
    <html>
    <head></head>
    <body>

    """

    for ip in config["ipv4"]:
        running_config = Config(ip=ip, type=ConfigType.RUNNING)
        startup_config = Config(ip=ip, type=ConfigType.STARTUP)

        ideal_config = Config(ip=ip, type=ConfigType.IDEAL)

        diff_ideal_startup = format_html(
            get_diff(str(ideal_config), str(startup_config))
        )
        diff_startup_running = format_html(
            get_diff(str(startup_config), str(running_config))
        )

        html_text += f"""

            <h1><b>Checking template vs. startup [{ip}]:</b></h1>
            <p>
                {diff_ideal_startup}
            </p>

        """
        html_text += f"""

            <h1><b>Checking startup vs. running [{ip}]:</b></h1>
            <p>
                {diff_startup_running}
            </p>

        """

    html_text += """
    </body>
    </html>
    """

    send_email(body=html_text)


if __name__ == "__main__":
    args = handle_aruments()
    if args.daemon:
        sys.stdout = open("/dev/null", "w")
        while True:
            main(args)
            time.sleep(1 * 60)
    else:
        main(args)
