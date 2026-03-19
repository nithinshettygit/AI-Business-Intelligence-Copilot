import requests
import json

URL = "http://localhost:8000/chat"
payload = {
    "query": "Build a dashboard for revenue",
    "history": []
}

try:
    response = requests.post(URL, json=payload)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("\n--- RESPONSE TEXT ---")
        print(data.get("text"))
        print("\n--- CHARTS ---")
        charts = data.get("charts", [])
        print(f"Number of charts: {len(charts)}")
        if charts:
            print(json.dumps(charts[0], indent=2)[:500] + "\n...")
            
    else:
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
