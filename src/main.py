from util import format_html, handle_aruments, load_config, format_bash
from cisco import (
    get_diff_ideal_startup,
    get_diff_startup_running,
    run_ansible,
    subprocess,
)


def send_email(body):
    body = format_bash(body)
    subprocess.run(
        [
            "ansible-playbook",
            "playbooks/send_mail.yml",
            "-e",
            f'body64={body}',
        ]
    )


def main2():
    args = handle_aruments()
    config = load_config(args.config)

    # run_ansible()
    html_text = """\
    <html>
    <head></head>
    <body>

    """

    for ip in config["ipv4"]:
        html_text += f"""

            <h1><b>Checking template vs. startup [{ip}]:</b></h1>
            <p>
                {format_html(get_diff_ideal_startup(f"{ip}"))}
            </p>

        """
        html_text += f"""

            <h1><b>Checking startup vs. running [{ip}]:</b></h1>
            <p>
                {format_html(get_diff_startup_running(f"{ip}"))}
            </p>

        """

    html_text += """
    </body>
    </html>
    """

    send_email(body=html_text)


if __name__ == "__main__":
    main2()
