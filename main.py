import requests
import json

###install librehardwaremonitor and get the ip, port, and then set that shi to this url
url = "http://192.999.99.99/data.json"

def find_cpu_info(nodes):
    cpu_info = []
    for node in nodes:
        if "Text" in node and "cpu" in node["Text"].lower():  
            cpu_info.append(node)  
          ###iterate throug
        if "Children" in node and isinstance(node["Children"], list):
            cpu_info.extend(find_cpu_info(node["Children"]))
    return cpu_info

try:
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()

            if not data:
                print("Received empty JSON response.")
            else:
                cpu_data = find_cpu_info(data.get("Children", []))

                temperature_list = []
                for sensor in cpu_data:
                    if sensor.get("Type") == "Temperature":
                        temperature_list.append(f"{sensor['Text']}: {sensor['Value']}°C")

                print(temperature_list)

        except ValueError:
            print("Error: JSON reponse is invalid.")
    else:
        print(f"HTTP Error found :( {response.status_code}")

except requests.exceptions.RequestException as e:
    print("Error getting CPU temperature data:", e)
