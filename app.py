import streamlit as st
import numpy as np
import pandas as pd
import json
import pydeck
from station_status import *

def calculate_color(row):
    base = row["capacity"]
    percentage = (row["bikes"] + row["ebikes"] + row["scooters"]) / base * 100  
    
    # Assign color based on percentage thresholds
    if percentage > 50:
        return [0, 255, 0]    # Green
    elif int(percentage) == 0:
        return [255, 0, 0]    # Red
    elif percentage < 50:
        return [255, 165, 0]  # Orange
    




url = "https://gbfs.lyft.com/gbfs/2.3/chi/en/station_information.json"
response = requests.get(url)
data = response.json()
data_frame = {"lat": [], "lon": [], "name": [], "capacity": [], "station_id": []}
for station in data["data"]["stations"]:
    data_frame["lat"].append(station["lat"])
    data_frame["lon"].append(station["lon"])
    data_frame["name"].append(station["name"])
    data_frame["capacity"].append(station["capacity"])
    data_frame["station_id"].append(station["station_id"])
df1 = pd.DataFrame(data_frame)

status_data = status()
df2 = pd.DataFrame(status_data)  

data_frame = df1.merge(df2, on="station_id", how="left")        
data_frame["color"] = data_frame.apply(calculate_color, axis=1)
map_data = pd.DataFrame(data_frame)

point_layer = pydeck.Layer(
    "ScatterplotLayer",
    data=map_data,
    id="Stations",
    get_position=["lon", "lat"],
    get_color = "color",
    pickable=True,
    auto_highlight=True,
    get_radius="100",
)

view_state=pydeck.ViewState(
        latitude=map_data["lat"].mean(), 
        longitude=map_data["lon"].mean(),
        zoom=10,
        pitch=0,
    )



chart = pydeck.Deck(
    point_layer,
    initial_view_state=view_state,
    tooltip={"text": "{name}, \nCapacity: {capacity}, \nAvailable bikes: {bikes}, \nAvailable e-bikes: {ebikes}, \nAvailable scooters: {scooters}"},
)


event = st.pydeck_chart(chart, on_select="rerun", selection_mode="multi-object")

event.selection