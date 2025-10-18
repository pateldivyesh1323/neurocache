import json

def log_status(timestamp, key, event, status = ""):
    log = {"timestamp": timestamp, "key": key, "event": event, "status": status}
    log_string = json.dumps(log)
    with open("data/access_log.jsonl", 'a') as file:
        file.write(f"{log_string}\n")