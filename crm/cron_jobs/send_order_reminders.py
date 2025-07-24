import logging
import datetime
from gql import gql, Client 
from gql.transport.requests import ResquestsHTTPTransport

# Configuration of the logger to write to the file /tmp/order_reminders_log.txt
logging.basicConfig(
    filename='/tmp/order_reminders_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
)

# Preparation of GraphQL transport to the endpoint
transport = ResquestsHTTPTransport(
    url='http://localhost:8000/graphql',
    verify=False,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculation of the current date and the date 7 days before
today = datetime.date.today()
seven_days_ago = today - datetime.timedelta(days=7)

# GraphQL query to obtain orders from the last 7 days
query = gql(f"""
            query {{
              orders(filter: {{
              orderDate_Gte: "{seven_days_ago}",
              orderDate_Lte: "{today}"
            }}) {{
            id
            customer {{
              email
            }}
        }}

    }}
    """)

try:
    result = client.execute(query)
    orders = result.get('orders', [])

    for order in orders:
        order_id = order['id']
        email = order['customer']['email']
        logging.info(f"Orders ID: {order_id}, Email: {email}")

    print("Order reminders processed")

except Exception as e:
    logging.error(f"Erreur lors de la recuperation des commandes : {e}")


