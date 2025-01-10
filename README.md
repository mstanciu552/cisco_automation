# Cisco Configuration Automation with Ansible, Python, and Telegram Bot

## Overview

This project automates the process of retrieving the configuration of a Cisco device using Ansible and Python. It allows you to compare the running configuration of the device with an ideal configuration and reports any differences. Additionally, it integrates with Telegram to send the results via a bot, making it easy to access the information from anywhere.

The Telegram bot provides several commands for easy access to configuration details and operations on the Cisco devices.

## Features

- **Retrieve Running Configuration**: Fetch the running configuration of a Cisco device using Ansible's networking modules.
- **Compare Configurations**: Compare the running configuration with a predefined ideal configuration.
- **Notify via Telegram**: Send a detailed report of the configuration comparison and any differences to a Telegram bot.
- **Customizable Ideal Config**: Easily modify the ideal configuration file to suit your network’s desired state.
- **Bot Commands**: The bot allows users to execute specific tasks related to configuration comparison and management directly through Telegram.

## Bot Commands

The Telegram bot supports the following commands:

- `/help`: Get a help message that explains the available commands and how to use them.
  
- `/diff_baseline {ip}`: Get the differences between the baseline configuration file and the startup configuration file of the device.  
   - **Example**: `/diff_baseline 192.168.1.1`

- `/diff_running {ip}`: Get the differences between the startup configuration file and the running configuration of the device.  
   - **Example**: `/diff_running 192.168.1.1`

- `/write_mem {ip}`: Write the running configuration to memory (save the running configuration to the startup configuration).  
   - **Example**: `/write_mem 192.168.1.1`

## Prerequisites

Before using this project, you will need to have the following installed:

1. **Python 3.x**  
   Install Python 3 if you haven't already:  
   https://www.python.org/downloads/

2. **Ansible**  
   Ansible is used for automating the retrieval of the device configuration. Install Ansible using pip:  
   ```bash
   pip install ansible
