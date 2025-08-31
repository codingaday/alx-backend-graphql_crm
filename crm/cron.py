import logging
from datetime import datetime
import requests

from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client

LOG_FILE = "/tmp/crm_heartbeat_log.txt"

import logging
from datetime import datetime
import requests

LOW_STOCK_LOG_FILE = "/tmp/low_stock_updates_log.txt"


def update_low_stock():
    """Calls the GraphQL mutation to restock low-stock products and logs the updates."""
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    mutation = """
    mutation {
      updateLowStockProducts {
        message
        updatedProducts {
          id
          name
          stock
        }
      }
    }
    """

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": mutation},
            timeout=10,
        )

        if response.ok:
            data = response.json().get("data", {}).get("updateLowStockProducts", {})
            message = data.get("message", "No message returned")
            updated = data.get("updatedProducts", [])

            with open(LOW_STOCK_LOG_FILE, "a") as f:
                f.write(f"[{timestamp}] {message}\n")
                for prod in updated:
                    f.write(
                        f"   Product: {prod['name']} | New stock: {prod['stock']}\n"
                    )

            logging.getLogger(__name__).info(f"Low stock update successful: {len(updated)} products.")
        else:
            err_msg = f"[{timestamp}] GraphQL mutation failed: {response.text}"
            with open(LOW_STOCK_LOG_FILE, "a") as f:
                f.write(err_msg + "\n")
            logging.error(err_msg)

    except Exception as e:
        with open(LOW_STOCK_LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] Exception: {e}\n")
        logging.error(f"Low stock update exception: {e}")



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
