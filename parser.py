import re

def parse_log(line):
    line = line.strip()

    # Failed login
    failed_pattern = r"Failed password for (invalid user )?(\w+) from (\d+\.\d+\.\d+\.\d+)"
    failed_match = re.search(failed_pattern, line)
    if failed_match:
        return {
            "event_type": "failed_login",
            "username": failed_match.group(2),
            "ip": failed_match.group(3),
            "status": "failed"
        }

    # Successful login
    success_pattern = r"Accepted password for (\w+) from (\d+\.\d+\.\d+\.\d+)"
    success_match = re.search(success_pattern, line)
    if success_match:
        return {
            "event_type": "successful_login",
            "username": success_match.group(1),
            "ip": success_match.group(2),
            "status": "success"
        }

    # sudo command usage
    sudo_pattern = r"sudo: (\w+)"
    sudo_match = re.search(sudo_pattern, line)
    if sudo_match:
        return {
            "event_type": "sudo_command",
            "username": sudo_match.group(1),
            "ip": "local",
            "status": "info"
        }

    return None
