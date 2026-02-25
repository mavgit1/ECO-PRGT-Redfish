import sys
import json
import requests
import urllib3

# Silence SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Get IP from PRTG parameter
ip = sys.argv[1]
url = f"https://{ip}/redfish/v1"

# Request
response = requests.get(url, verify=False)
data = response.json()

# JSON Output
print(json.dumps(data))