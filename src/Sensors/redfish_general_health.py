import argparse
import requests
import json
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run_sensor(ip, user, pwd):
    # Start timer and initialize fallback variables
    start_time = time.time()
    health = "Unknown"
    token = None
    session_url = None
    warning = ""

    try:
        with requests.Session() as s:
            s.verify = False
            s.timeout = 10
            base = f"https://{ip}/redfish/v1"

        
            # Login and get X-Auth-Token
            auth = s.post(f"{base}/SessionService/Sessions", json={"UserName": user, "Password": pwd}, verify=False)
            auth.raise_for_status() # Catches 401 Unauthorized or other HTTP errors
            token = auth.headers.get("X-Auth-Token")
            s.headers.update({"X-Auth-Token": token})
            session_url = f"https://{ip}{auth.json()['@odata.id']}"
            time.sleep(1)

            # Find system name / path
            sys_col = s.get(f"{base}/Systems").json()
            sys_url = f"https://{ip}{sys_col['Members'][0]['@odata.id']}"
            time.sleep(1)

            # Get health status
            data = s.get(sys_url).json()
            health = data.get("Status", {}).get("Health", "Unknown")
    
    finally:
        # If status not "ok" then error -> no "warning" state. Dell Standardlookups used: prtg.standardlookups.dell.dellstatus
        # 3 = OK (Green)
        # 4 = NonCritical (Yellow)
        # 5 = Critical (Red)
        status = 3 if health.lower() == "ok" else 5

        if token and session_url:
            time.sleep(1)
            try:
                requests.delete(session_url, headers={"X-Auth-Token": token}, verify=False, timeout=5)
            except Exception as e:
                status = 4
                warning = str(e)
                
        warning_msg = f" | Warning: {warning}" if warning else ""


    # Stop timer - all redfish requests are done
    end_time = time.time()
    exec_time_ms = int((end_time - start_time) * 1000)

    status_channel = {
        "channel": "Health Status",
        "value": status,
        "ValueLookup": "prtg.standardlookups.dell.dellstatus"
    }

    timer_channel = {
        "channel": "Execution Time",
        "value": exec_time_ms,
        "unit": "TimeResponse"
    }

    # PRTG output
    output = {
        "prtg": {
            "result": [
                status_channel,
                timer_channel
            ],
            # This prints the status message in "banner" below sensor name
            "text": f"Status is {health}{warning_msg}"
        }
    }
    return output

# Override parser logic so that messages are not printet in general allowing error messages to be raised to PRTG
# PRTG always expects a JSON and else would fail
class SilentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)
    def _print_message(self, message, file=None):
        pass

if __name__ == "__main__":
    try:
        parser = SilentParser(add_help=False)
        parser.add_argument('--ip', required=True)
        parser.add_argument('--user', required=True)
        parser.add_argument('--pwd', required=True)

        args = parser.parse_args()

        json_output = run_sensor(args.ip, args.user, args.pwd)
        print(json.dumps(json_output))


    except ValueError as e:
        print(json.dumps({
            "prtg": {
                "error": 1, 
                "text": f"Parameter Error: {str(e)}. Expected usage: --param1 VAL1 --param2 VAL2 ... --> all values best in quotes"
            }
        }))

    except Exception as e:
        print(json.dumps({
            "prtg": {
                "error": 1, 
                "text": f"Runtime Error: {str(e)}"
            }
        }))