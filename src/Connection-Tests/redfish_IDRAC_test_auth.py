import requests
import json
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# CONFIG
IDRAC_IP = "192.168.123.123"
USER = "manage"
PASS = "secret redactet here"

def test_login():
    url = f"https://{IDRAC_IP}/redfish/v1/SessionService/Sessions"
    payload = {"UserName": USER, "Password": PASS}
    
    # Just the POST, nothing else.
    response = requests.post(url, json=payload, verify=False)
    
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_login()