import streamlit as st
import numpy as np
import pandas as pd
import json
import pydeck
from station_status import *
from geopy.distance import geodesic

def calculate_color(row, type):
        
    if type == "rent":
        base = row["capacity"]
        percentage = (row["bikes"] + row["ebikes"] + row["scooters"]) / base * 100  
        
        # Assign color based on percentage thresholds
        if percentage > 50:
            return [0, 255, 0]    # Green
        elif int(percentage) == 0:
            return [255, 0, 0]    # Red
        elif percentage < 50:
            return [255, 165, 0]  # Orange
    elif type == "return":
        if row["return"] == 1:
            return [0, 255, 0]
        else:
            return [255, 0, 0]
    
def station_info():

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
    
    return data_frame


def create_chart(data, tooltip):
    point_layer = pydeck.Layer(
        "ScatterplotLayer",
        data=data,
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
            bearing=90,
        )



    chart = pydeck.Deck(
        point_layer,
        initial_view_state=view_state,
        tooltip=tooltip,
    )   

    return chart


def get_location():
    response = requests.get('https://ipinfo.io/')
    data = response.json()
    loc = data['loc'].split(',')
    lat = float(loc[0])
    lng = float(loc[1])
    city = data.get('city')
    country = data.get('country')
    location = (lat, lng, city, country)
    
    return location








station_info_data = station_info()
df1 = pd.DataFrame(station_info_data)


on = st.toggle("Return", help ="Click to see the stations accepting returns")
station_status_data = status_rent()
df2 = pd.DataFrame(station_status_data)  
data_frame = df1.merge(df2, on="station_id", how="left")        
data_frame["color"] = data_frame.apply(lambda row: calculate_color(row, "rent"), axis=1)
map_data = pd.DataFrame(data_frame)
tooltip = {"text": "{name}, \nCapacity: {capacity}, \nAvailable bikes: {bikes}, \nAvailable e-bikes: {ebikes}, \nAvailable scooters: {scooters}"}
chart = create_chart(map_data, tooltip)

if on:
    st.write("That's where you can return your vehicle. Turn off to get back")
    station_status_data = status_return()
    df2 = pd.DataFrame(station_status_data)  
    data_frame = df1.merge(df2, on="station_id", how="left")        
    data_frame["color"] = data_frame.apply(lambda row: calculate_color(row, "return"), axis=1)
    map_data = pd.DataFrame(data_frame)
    tooltip = {"text": "{name}"}
    chart = create_chart(map_data, tooltip)


event = st.pydeck_chart(chart, on_select="rerun", selection_mode="multi-object")

event.selection

option = st.selectbox(
    "Detailed overview, sort by:",
    ("Availability", "Station name", "Current location"),
    index=None,
    placeholder="Select filtering option...",
)

if option == "Availability":
    st.dataframe(
    map_data.assign(percentage=(map_data["bikes"] + map_data["ebikes"] + map_data["scooters"]) / map_data["capacity"] * 100)
    .sort_values(by="percentage", ascending=True)
)
    
elif option == "Station name":
    station_list = st.selectbox(
    "Enter your area:",
    (map_data["name"]),
    index=None,
    placeholder="Select filtering option...",
)

elif option == "Current location":
    location = get_location()
    lat = location[0]
    lng = location[1]
    #user_location = (lat, lng)
    user_location = (41.96648, -87.78202)
    map_data["distance_km"] = map_data.apply(lambda row: geodesic((row["lat"], row["lon"]), user_location).km, axis=1)

    #filtered_stations = map_data[(map_data["lat"] == lat) & (map_data["lon"] == lng)]
    filtered_stations = map_data[map_data["distance_km"] <= 1]
    st.dataframe(filtered_stations)

else:
    st.dataframe(map_data, column_config={"color" :None, "station_id" :None,"lat": None, "lon": None })


