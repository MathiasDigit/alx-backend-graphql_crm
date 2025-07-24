from celery import shared_task
import requests
from datetime import datetime

@shared_task
def generate_crm_report():
    graphql_url = "http://localhost:8000/graphql/"  # À adapter si nécessaire

    query = '''
    query {
        totalCustomers
        totalOrders
        totalRevenue
    }
    '''

    try:
        response = requests.post(graphql_url, json={'query': query})
        data = response.json()

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_path = "/tmp/crm_report_log.txt"

        if 'errors' in data:
            with open(log_path, 'a') as f:
                f.write(f"[{now}] ❌ Erreurs : {data['errors']}\n")
        else:
            result = data['data']
            line = (f"[{now}] ✅ Rapport : {result['totalCustomers']} clients, "
                    f"{result['totalOrders']} commandes, "
                    f"{result['totalRevenue']} €\n")
            with open(log_path, 'a') as f:
                f.write(line)

    except Exception as e:
        with open("/tmp/crm_report_log.txt", 'a') as f:
            f.write(f"[{now}] ❗ Exception : {str(e)}\n")
