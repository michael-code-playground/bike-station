import numpy as np
import pandas as pd
import json
import requests
def status_rent():
    data_frame = {"station_id": [], "bikes": [], "ebikes": [], "scooters" :[]}
    url = "https://gbfs.lyft.com/gbfs/2.3/chi/en/station_status.json"
    response = requests.get(url)
    
    data = response.json()
    for station in data["data"]["stations"]:
        station_id = station["station_id"]
    
        num_scooters = station.get("num_scooters_available",0)
    
        vehicle_types = station.get("vehicle_types_available")
        data_frame["station_id"].append(station_id)
        data_frame["scooters"].append(num_scooters)
    
        data_frame["bikes"].append(vehicle_types[0].get("count"))
        data_frame["ebikes"].append(vehicle_types[1].get("count"))
    
        
    return data_frame


def status_return():
    data_frame = {"station_id": [], "return": []}
    url = "https://gbfs.lyft.com/gbfs/2.3/chi/en/station_status.json"
    response = requests.get(url)
    
    data = response.json()
    for station in data["data"]["stations"]:
        station_id = station["station_id"]
        return_status = station["is_returning"]
        data_frame["station_id"].append(station_id)
        data_frame["return"].append(return_status)
    return data_frame