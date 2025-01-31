import requests
import json
import time

with open('feed.json') as json_file:
    
    data = json.load(json_file)
    
    for feed in data["data"]["en"]["feeds"]:
        
        url = feed["url"]
        name = feed["name"]

    # Make a GET request to the URL
        response = requests.get(url)
        time.sleep(3)
    # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()  # Parse JSON response
            
            data = response.text
            with open(name+".json", "w") as file:
                file.write(data)
        else:
            print(f"Error: Unable to fetch data (Status code: {response.status_code})")
