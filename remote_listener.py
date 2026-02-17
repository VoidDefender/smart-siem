import socket
import threading
import os
from dotenv import load_dotenv
from parser import parse_log
from database import insert_log
from rule_engine import evaluate_rules
from logger import get_logger

# ---------------------------------------------------
# Load environment variables
# ---------------------------------------------------
load_dotenv()

logger = get_logger("remote_listener")

HOST = "0.0.0.0"
START_PORT = int(os.getenv("REMOTE_PORT", 9000))

failed_tracker = {}

# ---------------------------------------------------
# Find Available Port
# ---------------------------------------------------
def find_free_port(start_port):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((HOST, port))
                return port
            except OSError:
                port += 1

# ---------------------------------------------------
# Handle Incoming Client
# ---------------------------------------------------
def handle_client(conn, addr):
    logger.info(f"Connection established from {addr}")

    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break

            log_line = data.decode().strip()
            logger.info(f"Received remote log: {log_line}")

            parsed = parse_log(log_line)

            if parsed:
                insert_log(parsed)
                evaluate_rules(parsed, failed_tracker)

    except Exception as e:
        logger.error(f"Error handling client {addr}: {e}")

    finally:
        conn.close()
        logger.info(f"Connection closed: {addr}")

# ---------------------------------------------------
# Start TCP Server
# ---------------------------------------------------
def start_server():
    port = find_free_port(START_PORT)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, port))
    server.listen(10)

    logger.info(f"Remote log listener started on port {port}")
    print(f"[+] Remote listener running on port {port}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon = True
        thread.start()

# ---------------------------------------------------
# Entry Point
# ---------------------------------------------------
if __name__ == "__main__":
    start_server()
