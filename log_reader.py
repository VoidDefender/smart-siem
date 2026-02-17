from state_manager import get_last_position, update_position

def read_logs(file_path):
    logs = []
    last_position = get_last_position()

    with open(file_path, "r") as file:
        file.seek(last_position)

        for line in file:
            logs.append(line)

        current_position = file.tell()

    update_position(current_position)

    return logs
