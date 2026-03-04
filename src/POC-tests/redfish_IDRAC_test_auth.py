import requests
import json
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# CONFIG
IDRAC_IP = "123.123.123.123"
USER = "username"
PASS = "password"

def test_login():
    url = f"https://{IDRAC_IP}/redfish/v1/SessionService/Sessions"
    payload = {"UserName": USER, "Password": PASS}

    response = requests.post(url, json=payload, verify=False)

    # For actual further requests the session token must be retrieved - this later can be used
    # response.headers.get("X-Auth-Token")
    # headers = {"X-Auth-Token": token}
    #
    # eg. get Systems: requests.get(f"{base}/Systems", headers=headers, verify=False).json()
    
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_login()