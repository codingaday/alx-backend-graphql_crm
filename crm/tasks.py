import logging
from datetime import datetime
import requests
from celery import shared_task

LOG_FILE = "/tmp/crm_report_log.txt"

@shared_task
def generate_crm_report():
    """Weekly CRM report: total customers, orders, and revenue."""

    query = """
    query {
      customers {
        id
      }
      orders {
        id
        totalAmount
      }
    }
    """

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": query},
            timeout=10,
        )
        if response.ok:
            data = response.json().get("data", {})

            customers = data.get("customers", [])
            orders = data.get("orders", [])
            total_customers = len(customers)
            total_orders = len(orders)
            total_revenue = sum(float(o.get("totalAmount", 0)) for o in orders)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            report_line = (
                f"{timestamp} - Report: "
                f"{total_customers} customers, {total_orders} orders, {total_revenue} revenue"
            )

            with open(LOG_FILE, "a") as f:
                f.write(report_line + "\n")

            logging.getLogger(__name__).info(report_line)
        else:
            logging.error(f"GraphQL query failed: {response.text}")

    except Exception as e:
        logging.error(f"CRM report generation failed: {e}")
