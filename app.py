from log_reader import read_logs
from parser import parse_log
from database import insert_log
from rule_engine import evaluate_rules
from logger import get_logger

logger = get_logger("app")

def main():
    logs = read_logs("auth.log")

    logger.info("Log processing started.")

    event_count = 0
    failed_tracker = {}

    for log in logs:
        parsed = parse_log(log)
        if parsed:
            insert_log(parsed)
            evaluate_rules(parsed, failed_tracker)
            event_count += 1

    logger.info(f"Total security events processed: {event_count}")

if __name__ == "__main__":
    main()
