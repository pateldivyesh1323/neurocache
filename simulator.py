import json
import random
import time
from collections import defaultdict

def simulate_cache_workload(
    num_sessions=5,
    num_keys=50,
    num_requests=1000,
    hot_key_ratio=0.2,
    get_prob=0.7
):
    sessions = [f"session_{i}" for i in range(num_sessions)]
    keys = [f"key_{i}" for i in range(num_keys)]

    # hot keys get accessed more frequently
    hot_keys = random.sample(keys, int(num_keys * hot_key_ratio))

    # tracking structures
    last_access_time = defaultdict(lambda: None)
    access_count = defaultdict(int)

    events = []
    current_time = time.time()

    for _ in range(num_requests):
        session = random.choice(sessions)
        # bias towards hot keys
        key = random.choice(hot_keys) if random.random() < 0.6 else random.choice(keys)
        event = "get" if random.random() < get_prob else "set"

        # cache hit/miss
        if event == "get":
            status = "hit" if random.random() < 0.7 else "miss"
        else:
            status = ""

        # simulate time gaps between requests (0.1s–3s)
        current_time += random.uniform(0.1, 3.0)

        # derived metrics
        if last_access_time[key] is not None:
            time_since_last_access = current_time - last_access_time[key]
        else:
            time_since_last_access = 0.0  # first access

        access_count[key] += 1
        last_access_time[key] = current_time

        events.append({
            "session": session,
            "timestamp": current_time,
            "key": key,
            "event": event,
            "status": status,
            "time_since_last_access": round(time_since_last_access, 4),
            "access_count": access_count[key],
        })

    # Write to JSONL file
    with open("./data/access_log.jsonl", "w") as f:
        for e in events:
            f.write(json.dumps(e) + "\n")

    print(f"✅ Generated {len(events)} events across {num_sessions} sessions.")
    print("📁 File saved as ./data/simulated_cache_log.jsonl")

if __name__ == "__main__":
    simulate_cache_workload()
