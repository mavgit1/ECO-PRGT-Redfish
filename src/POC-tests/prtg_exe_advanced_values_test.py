import argparse
import sys
import json
import random

def generate_fake_data(use_defaults):
    try:
        # Simulate a crash ~10% of the time
        if random.random() < 0.1:
            raise Exception("Random simulated sensor error!")

        temp = random.randint(30, 95)
        cpu = random.randint(10, 100)
        status = random.choice([3, 4, 5]) 

        # Define Channels
        temp_channel = {
            "channel": "Temperature",
            "value": temp,
            "unit": "Custom",
            "customunit": "C"
        }
        
        cpu_channel = {
            "channel": "CPU Load",
            "value": cpu,
            "unit": "Percent"
        }

        status_channel = {
            "channel": "Health Status",
            "value": status,
            "ValueLookup": "prtg.standardlookups.dell.dellstatus"
        }

        # If "use_defaults" flag true inject limits
        # Example for lower bounds:
        # "LimitMinWarning": 10,  
        # "LimitMinError": 5
        if use_defaults:
            temp_channel.update({
                "LimitMode": 1,
                "LimitMaxWarning": 55,
                "LimitMaxError": 70
            })
            cpu_channel.update({
                "LimitMode": 1,
                "LimitMaxWarning": 60,
                "LimitMaxError": 70
            })

        # Create output JSON for PRTG
        output = {
            "prtg": {
                "result": [
                    temp_channel,
                    cpu_channel,
                    status_channel

                ],
                "text": f"Small text that will displlay on title bar.  Can eg. send values --> TEMP {temp}C, CPU: {cpu}% but usually left empty. Could also be uused for custom Messages."
            }
        }
        
        print(json.dumps(output))

    except Exception as e:
        print(json.dumps({"prtg": {"error": 1, "text": str(e)}}))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PRTG Value Example Sensor")

    # Argument "limits" to enable or disable limits when calling the sensor
    parser.add_argument(
        '--limits', 
        type=str.lower, 
        choices=['true', 'false'], 
        default='false'
    )

    args = parser.parse_args()

    enable_limits = (args.limits == 'true')

    generate_fake_data(enable_limits)