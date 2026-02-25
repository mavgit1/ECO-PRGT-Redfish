import requests
import json
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run_sensor(ip, user, pwd):
    try:
        base = f"https://{ip}/redfish/v1"
        
        # 1. Login
        auth = requests.post(f"{base}/SessionService/Sessions", 
                             json={"UserName": user, "Password": pwd}, 
                             verify=False, timeout=10)
        token = auth.headers.get("X-Auth-Token")
        headers = {"X-Auth-Token": token}

        # 2. Find System
        sys_col = requests.get(f"{base}/Systems", headers=headers, verify=False).json()
        sys_url = f"https://{ip}{sys_col['Members'][0]['@odata.id']}"
        
        # 3. Get Health
        data = requests.get(sys_url, headers=headers, verify=False).json()
        health = data.get("Status", {}).get("Health", "Unknown")

        # Map string to numeric (0=OK, 1=Warning, 2=Critical)
        val = 0 if health == "OK" else 1 if health == "Warning" else 2

        # 4. PRTG Output
        output = {
            "prtg": {
                "result": [
                    {
                        "channel": "System Health",
                        "value": val,
                        "unit": "Custom",
                        "customunit": "Status"
                    }
                ],
                "text": f"Status is {health}"
            }
        }
        print(json.dumps(output))

    except Exception as e:
        # Returns an error state to PRTG if the script fails
        print(json.dumps({"prtg": {"error": 1, "text": f"Script Error: {str(e)}"}}))

if __name__ == "__main__":
    # Pass parameters from PRTG: %host %windowsuser %windowspassword
    run_sensor(sys.argv[1], sys.argv[2], sys.argv[3])