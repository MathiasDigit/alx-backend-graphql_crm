import requests
from datetime import datetime
from datetime import datetime
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client


def log_crm_heartbeat():
    now = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{now} CRM is alive\n"

    with open("./crm_heartbeat_log.txt", "a") as f:
        f.write(message)

if __name__ == "__main__":
    log_crm_heartbeat()

def update_low_stock():
    graphql_endpoint = "http://localhost:8000/graphql/"  # URL de ton endpoint GraphQL
    mutation = '''
    mutation {
        updateLowStockProducts {
            message
            updatedProducts {
                name
                stock
            }
        }
    }
    '''

    try:
        response = requests.post(graphql_endpoint, json={'query': mutation})
        data = response.json()

        log_path = "/tmp/low_stock_updates_log.txt"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_path, "a") as f:
            if "errors" in data:
                f.write(f"[{now}] ❌ Erreur : {data['errors']}\n")
            else:
                updates = data["data"]["updateLowStockProducts"]["updatedProducts"]
                msg = data["data"]["updateLowStockProducts"]["message"]
                f.write(f"[{now}] ✅ {msg}\n")
                for product in updates:
                    f.write(f"    - {product['name']} => Stock: {product['stock']}\n")

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"[{now}] ❗ Exception : {str(e)}\n")
