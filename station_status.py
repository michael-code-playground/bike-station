import numpy as np
import pandas as pd
import json

def status():
    data_frame = {"station_id": [], "bikes": [], "ebikes": [], "scooters" :[]}
    with open('station_status.json') as json_file:
        data = json.load(json_file)
        for station in data["data"]["stations"]:
            station_id = station["station_id"]
    #print(station_id)
            num_scooters = station.get("num_scooters_available",0)
    #print(num_scooters)
            vehicle_types = station.get("vehicle_types_available")
            data_frame["station_id"].append(station_id)
            data_frame["scooters"].append(num_scooters)
    #print(vehicle_types)
            data_frame["bikes"].append(vehicle_types[0].get("count"))
            data_frame["ebikes"].append(vehicle_types[1].get("count"))
    #for vehicle_type in vehicle_types:
        #print(vehicle_type)
        
    return data_frame
#print(data_frame)


