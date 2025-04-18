import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.distance import great_circle

# Load the trained model
model = pickle.load(open("uber_trip_model.sav", 'rb'))

st.title("🚖 Uber Fare Prediction App")

# Input form
st.header("Enter trip details")

geolocator = Nominatim(user_agent='geoapiExercise')

def get_coordinates(location):
    try:
        location_data = geolocator.geocode(location)
        if location_data:
            return location_data.latitude, location_data.longitude
        else:
            st.error("Location not found")
            return None, None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, None

def get_distance(pickup_lat, pickup_long, dropoff_lat, dropoff_long):
    loc1 = (pickup_lat, pickup_long)
    loc2 = (dropoff_lat, dropoff_long)
    return great_circle(loc1, loc2).km

def get_dayperiod(hour):
    if 5 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Afternoon'
    elif 17 <= hour < 22:
        return 'Evening'
    else:
        return 'Night'

def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

# Get input locations from user
pickup_location = st.text_input('Pickup Location')
dropoff_location = st.text_input('Dropoff Location')

if pickup_location and dropoff_location:
    pickup_latitude, pickup_longitude = get_coordinates(pickup_location)
    dropoff_latitude, dropoff_longitude = get_coordinates(dropoff_location)

    if pickup_latitude is not None and dropoff_latitude is not None:
        current_datetime = datetime.now()
        
        year = current_datetime.year
        month = current_datetime.month
        week_day = current_datetime.weekday()
        hour = current_datetime.hour
        season = get_season(month)
        day_period = get_dayperiod(hour)

        # Calculate the distance
        distance = get_distance(pickup_latitude, pickup_longitude, dropoff_latitude, dropoff_longitude)

        # Prepare the data for prediction
        input_data = pd.DataFrame([[1, year, month, week_day, hour, season, day_period, distance]],
                                columns=['passenger_count', 'pickup_year', 'pickup_month', 'pickup_weekday',
                                        'pickup_hour', 'pickup_Season', 'pickup_dayperiod', 'Distance'])

        # Make the prediction
        fare = model.predict(input_data)

        # Display the result
        st.subheader(f"Distance from {pickup_location} to {dropoff_location}: {distance:.2f} km")
        st.subheader(f"Predicted Fare: ${fare[0]}")
    else:
        st.error("Could not retrieve coordinates for the provided locations. Please check the inputs.")
