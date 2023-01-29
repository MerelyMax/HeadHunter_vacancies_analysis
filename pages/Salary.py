import streamlit as st
import json
import os
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="Salaries analysis", page_icon="📈")

# Function to extract data fron .json file
def extract_json_file(file_name):
    f = open(file_name, mode='r', encoding='utf8')
    return json.loads('[' + f.read() + ']')

# Extracting data
data = extract_json_file(os.path.dirname(__file__) + '/vacancies_data.json')
df_data = pd.DataFrame(data)

# Adding interactive filters
job_counts_by_area = df_data['area-name'].value_counts()
city_choice = st.sidebar.selectbox(
    'Choose city:', 
    job_counts_by_area[job_counts_by_area.values > 10].keys())
currency_choice = st.sidebar.selectbox(
    'Choose currency:', 
    df_data['salary-currency'].dropna().unique())

# Constructing plots
hist1 = alt.Chart(df_data['salary-from'][(df_data['area-name'] == city_choice) & 
                                        (df_data['salary-currency'] == currency_choice)].to_frame()
                  ).mark_bar().encode(alt.X('salary-from:Q', bin = True),
                                                y = 'count()',
                                    )
st.altair_chart(hist1)

hist2 = alt.Chart(df_data['salary-to'][(df_data['area-name'] == city_choice) & 
                                        (df_data['salary-currency'] == currency_choice)].to_frame()
                  ).mark_bar().encode(alt.X('salary-to:Q', bin = True),
                                            y = 'count()',
                                    )
st.altair_chart(hist2)
# Showing statistics
salary_from_stats = df_data['salary-from'][(df_data['area-name'] == city_choice) & 
                        (df_data['salary-currency'] == currency_choice)].describe().to_frame()
salary_to_stats = df_data['salary-to'][(df_data['area-name'] == city_choice) & 
                    (df_data['salary-currency'] == currency_choice)].describe().to_frame()

col1, col2 = st.columns(2)
    
with col1:
    st.write("Statistics for Salary-From")
    st.dataframe(salary_from_stats)
with col2:
    st.write("Statistics for Salary-To")
    st.dataframe(salary_to_stats)



