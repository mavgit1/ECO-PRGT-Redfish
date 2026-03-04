import sys
import json
import requests
import urllib3

# Surpress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# IP MUSST BE PASSED AS PARAMETER TO .exe (eg. ..test.exe "192.168.1.1")
ip = sys.argv[1]
url = f"https://{ip}/redfish/v1"

response = requests.get(url, verify=False)
data = response.json()

print(json.dumps(data))