#!/usr/bin/env python3
"""
Order Reminder Script
Fetches pending orders from the GraphQL endpoint
and logs reminders with customer emails.
"""

import sys
import logging
from datetime import datetime, timedelta
import asyncio
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Configure logging
LOG_FILE = "/tmp/order_reminders_log.txt"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [INFO] %(message)s",
)

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

# Calculate cutoff date (7 days ago)
cutoff_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

# GraphQL query
query = gql(
    """
    query getRecentOrders($cutoffDate: Date!) {
      orders(orderDate_Gte: $cutoffDate) {
        id
        customer {
          email
        }
      }
    }
    """
)


async def fetch_and_log_orders():
    try:
        transport = RequestsHTTPTransport(
            url=GRAPHQL_URL,
            verify=True,
            retries=3,
        )
        async with Client(transport=transport, fetch_schema_from_transport=True) as session:
            result = await session.execute(query, variable_values={"cutoffDate": cutoff_date})
            orders = result.get("orders", [])

            if not orders:
                logging.info("No recent orders found.")
            else:
                for order in orders:
                    order_id = order["id"]
                    customer_email = order["customer"]["email"]
                    logging.info(f"Order ID: {order_id}, Customer Email: {customer_email}")

            print("Order reminders processed!")

    except Exception as e:
        logging.error(f"Error fetching orders: {e}")
        print("Failed to process order reminders!", file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(fetch_and_log_orders())
