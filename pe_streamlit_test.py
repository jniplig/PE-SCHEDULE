import streamlit as st
import pandas as pd

# Upload the Excel file
from google.colab import files
uploaded = files.upload()

# Load the data
file_path = list(uploaded.keys())[0]
block_4_data = pd.read_excel(file_path, sheet_name='Block 4')

# Rename columns for readability
block_4_data.columns = [
    "Day_Sorted", "Day", "Secondary_Period", "Division", "Year_Group",
    "Start_Time", "End_Time", "Duration", "Class_Set", "Squad",
    "PE_Teacher", "Location"
]

st.title('PE Department Timetable')

# Create a copy of the data for filtering
filtered_data = block_4_data.copy()

# Create filters for the data
day = st.sidebar.multiselect('Day', filtered_data['Day'].unique())
if day:
    filtered_data = filtered_data[filtered_data['Day'].isin(day)]

period = st.sidebar.multiselect('Secondary Period', filtered_data['Secondary_Period'].unique())
if period:
    filtered_data = filtered_data[filtered_data['Secondary_Period'].isin(period)]

division = st.sidebar.multiselect('Division', filtered_data['Division'].unique())
if division:
    filtered_data = filtered_data[filtered_data['Division'].isin(division)]

year_group = st.sidebar.multiselect('Year Group', filtered_data['Year_Group'].dropna().unique())
if year_group:
    filtered_data = filtered_data[filtered_data['Year_Group'].isin(year_group)]

class_set = st.sidebar.multiselect('Class', filtered_data['Class_Set'].dropna().unique())
if class_set:
    filtered_data = filtered_data[filtered_data['Class_Set'].isin(class_set)]

squad = st.sidebar.multiselect('Squad', filtered_data['Squad'].dropna().unique())
if squad:
    filtered_data = filtered_data[filtered_data['Squad'].isin(squad)]

teacher = st.sidebar.multiselect('PE Teacher', filtered_data['PE_Teacher'].dropna().unique())
if teacher:
    filtered_data = filtered_data[filtered_data['PE_Teacher'].isin(teacher)]

location = st.sidebar.multiselect('Location', filtered_data['Location'].dropna().unique())
if location:
    filtered_data = filtered_data[filtered_data['Location'].isin(location)]

st.dataframe(filtered_data)

st.sidebar.write('Filters applied:')
st.sidebar.write(f'Day: {day}')
st.sidebar.write(f'Secondary Period: {period}')
st.sidebar.write(f'Division: {division}')
st.sidebar.write(f'Year Group: {year_group}')
st.sidebar.write(f'Class: {class_set}')
st.sidebar.write(f'Squad: {squad}')
st.sidebar.write(f'Teacher: {teacher}')
st.sidebar.write(f'Location: {location}')
