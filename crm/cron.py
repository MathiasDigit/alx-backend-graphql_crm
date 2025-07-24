from datetime import datetime

def log_crm_heartbeat():
    now = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{now} CRM is alive\n"

    with open("/crom/crm_heartbeat_log.txt", "a") as f:
        f.write(message)