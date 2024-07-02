import streamlit as st
import pandas as pd
import altair as alt

# Load the data directly from the local file
file_path = 'PE DEPT HOURS - STREMLIT.xlsx'
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

# Summary Statistics
st.write("Summary Statistics:")
st.write(f"Total Classes: {filtered_data.shape[0]}")
st.write(f"Average Duration: {filtered_data['Duration'].mean()}")

# Bar chart of the number of classes per period
period_class_count = filtered_data['Secondary_Period'].value_counts().reset_index()
period_class_count.columns = ['Secondary_Period', 'Class_Count']

bar_chart = alt.Chart(period_class_count).mark_bar().encode(
    x='Secondary_Period',
    y='Class_Count'
).properties(
    title='Number of Classes per Period'
)

st.altair_chart(bar_chart, use_container_width=True)

# Export filtered data as CSV
@st.cache
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv_data = convert_df_to_csv(filtered_data)

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv_data,
    file_name='filtered_timetable_data.csv',
    mime='text/csv',
)
