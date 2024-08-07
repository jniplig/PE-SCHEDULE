import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

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

# Function to create checkbox filter within an expander
def create_checkbox_filter(expander, column_name, df):
    unique_values = df[column_name].dropna().unique()
    selected_values = []
    for value in unique_values:
        if expander.checkbox(f'{value}', key=f'{column_name}_{value}'):
            selected_values.append(value)
    return selected_values

# Create expandable sections for filters
day_expander = st.sidebar.expander("Filter by Day")
selected_days = create_checkbox_filter(day_expander, 'Day', block_4_data)
if selected_days:
    block_4_data = block_4_data[block_4_data['Day'].isin(selected_days)]

period_expander = st.sidebar.expander("Filter by Secondary Period")
selected_periods = create_checkbox_filter(period_expander, 'Secondary_Period', block_4_data)
if selected_periods:
    block_4_data = block_4_data[block_4_data['Secondary_Period'].isin(selected_periods)]

division_expander = st.sidebar.expander("Filter by Division")
selected_divisions = create_checkbox_filter(division_expander, 'Division', block_4_data)
if selected_divisions:
    block_4_data = block_4_data[block_4_data['Division'].isin(selected_divisions)]

year_group_expander = st.sidebar.expander("Filter by Year Group")
selected_year_groups = create_checkbox_filter(year_group_expander, 'Year_Group', block_4_data)
if selected_year_groups:
    block_4_data = block_4_data[block_4_data['Year_Group'].isin(selected_year_groups)]

class_expander = st.sidebar.expander("Filter by Class")
selected_classes = create_checkbox_filter(class_expander, 'Class_Set', block_4_data)
if selected_classes:
    block_4_data = block_4_data[block_4_data['Class_Set'].isin(selected_classes)]

squad_expander = st.sidebar.expander("Filter by Squad")
selected_squads = create_checkbox_filter(squad_expander, 'Squad', block_4_data)
if selected_squads:
    block_4_data = block_4_data[block_4_data['Squad'].isin(selected_squads)]

teacher_expander = st.sidebar.expander("Filter by PE Teacher")
selected_teachers = create_checkbox_filter(teacher_expander, 'PE_Teacher', block_4_data)
if selected_teachers:
    block_4_data = block_4_data[block_4_data['PE_Teacher'].isin(selected_teachers)]

location_expander = st.sidebar.expander("Filter by Location")
selected_locations = create_checkbox_filter(location_expander, 'Location', block_4_data)
if selected_locations:
    block_4_data = block_4_data[block_4_data['Location'].isin(selected_locations)]

st.dataframe(block_4_data)

# Summary Statistics
st.write("Summary Statistics:")
st.write(f"Total Classes: {block_4_data.shape[0]}")

# Bar chart of the number of classes per period
period_class_count = block_4_data['Secondary_Period'].value_counts().reset_index()
period_class_count.columns = ['Secondary_Period', 'Class_Count']

bar_chart = alt.Chart(period_class_count).mark_bar().encode(
    x='Secondary_Period',
    y='Class_Count'
).properties(
    title='Number of Classes per Period'
)

st.altair_chart(bar_chart, use_container_width=True)

# Interactive scatter plot with hover information
fig = px.scatter(block_4_data, x='Start_Time', y='Day', color='PE_Teacher', hover_data=['Class_Set', 'Year_Group', 'Location'])
fig.update_layout(title='Class Schedule', xaxis_title='Start Time', yaxis_title='Day')
st.plotly_chart(fig)

# Export filtered data as CSV
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv_data = convert_df_to_csv(block_4_data)

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv_data,
    file_name='filtered_timetable_data.csv',
    mime='text/csv',
)
