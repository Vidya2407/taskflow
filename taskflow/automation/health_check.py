import requests
import time
import datetime

APP_URL = "http://52.73.114.168:5000/health"
CHECK_INTERVAL = 60

def check_health():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        response = requests.get(APP_URL, timeout=10)
        if response.status_code == 200:
            print(f"[{timestamp}] ✅ App is healthy - Response time: {response.elapsed.total_seconds():.2f}s")
        else:
            print(f"[{timestamp}] ⚠️ App returned status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"[{timestamp}] ❌ App is DOWN - Connection refused")
    except requests.exceptions.Timeout:
        print(f"[{timestamp}] ❌ App is DOWN - Timeout")

if __name__ == "__main__":
    print("Starting TaskFlow health monitor...")
    print(f"Checking every {CHECK_INTERVAL} seconds")
    print("-" * 50)
    while True:
        check_health()
        time.sleep(CHECK_INTERVAL)