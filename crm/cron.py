import logging
from datetime import datetime
import requests

LOG_FILE = "/tmp/crm_heartbeat_log.txt"


def log_crm_heartbeat():
    """Logs a heartbeat message every 5 minutes and checks GraphQL hello field."""
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    try:
        # Optional: check GraphQL hello field
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5,
        )
        if response.ok and "data" in response.json():
            hello_msg = response.json()["data"].get("hello", "")
            message += f" | GraphQL says: {hello_msg}"
        else:
            message += " | GraphQL check failed"
    except Exception as e:
        message += f" | GraphQL error: {e}"

    # Append to log file
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

    # Also log to Django’s logger (optional)
    logging.getLogger(__name__).info(message)
