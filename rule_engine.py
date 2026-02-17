from database import insert_alert
from email_notifier import send_email_alert
from logger import get_logger

logger = get_logger("rule_engine")

def evaluate_rules(event, failed_tracker):

    # Rule 1: Brute Force (3 failed attempts from same IP)
    if event["event_type"] == "failed_login":
        ip = event["ip"]
        failed_tracker[ip] = failed_tracker.get(ip, 0) + 1

        if failed_tracker[ip] == 3:
            message = f"Brute force suspected from {ip}"

            insert_alert(
                "brute_force",
                event["username"],
                ip,
                message,
                "HIGH"
            )

            logger.warning(f"Brute force detected from {ip}")

    # Rule 2: Root login attempt (CRITICAL + Email)
    if event["event_type"] == "failed_login" and event["username"] == "root":
        message = f"Failed login attempt on ROOT account from {event['ip']}"

        insert_alert(
            "root_attack",
            event["username"],
            event["ip"],
            message,
            "CRITICAL"
        )

        logger.critical("Root account attack detected")

        # Send email alert
        send_email_alert(
            subject="CRITICAL ALERT - ROOT ATTACK DETECTED",
            body=message
        )
