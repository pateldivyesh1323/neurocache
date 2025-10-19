import json

def log_status(session, timestamp, key, event, status = "", time_since_last_access = None, access_count = None):
    log_data = {
        "session": session, 
        "timestamp": timestamp, 
        "key": key, 
        "event": event, 
        "status": status, 
        "time_since_last_access": time_since_last_access, 
        "access_count": access_count
    }
    log_string = json.dumps(log_data)
    with open("data/access_log.jsonl", 'a') as file:
        file.write(f"{log_string}\n")