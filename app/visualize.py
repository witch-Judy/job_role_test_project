from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from src.analysis.framework import framework
from src.analysis.job_title import title
from src.analysis.country_income import country_income

filename2020 = './data/raw/kaggle_survey_2020_responses.csv'
filename2021 = './data/raw/kaggle_survey_2021_responses.csv'
filename2022 = './data/raw/kaggle_survey_2022_responses.csv'

df0 = pd.read_csv(filename2020, low_memory=False)
df1 = pd.read_csv(filename2021, low_memory=False)
df2 = pd.read_csv(filename2022, low_memory=False)

df0['year'] = 2020
df1['year'] = 2021
df2['year'] = 2022


# country_earn = country_income(df0, df1, df2, year, country)

title_of_top5 = title(df0, df1, df2)
pop_framework = framework(df0, df1, df2)


st.header("Data Science and Machine Learning")
st.header("Industry Survey 2020-2022", divider='blue')
# page = st.sidebar.selectbox('Select a Page:', ['Trend', 'Statistics'])

tab1, tab2 = st.tabs(["Trends", "Statistics"])

with tab1:
    st.header("Trends")
    st.write('Top five job titles of the respondants')
    selected_titles = st.multiselect('Select job titles to display their trends:', title_of_top5['title'], 'Student')

    # Filter the DataFrame for the selected title
    title_data = title_of_top5[title_of_top5['title'].isin(selected_titles)]

    # Create a line plot for the selected title
    # if not title_data.empty:
    st.line_chart(title_data.set_index('title').T)

    # Display a bar chart for the selected title
    st.bar_chart(title_data.set_index('title').T)

with tab2:
    st.header("Statistics")
    labelx = ['Age Composition', 'Level of Income', 'Popular ML Framework']
    x = st.selectbox("Which trend do you want to see?",labelx,0)
    timeframe = st.slider("Select the time frame", 2020, 2023, (2020,2023))
    year0 = st.checkbox('2020')
    year1 = st.checkbox('2021')
    year2 = st.checkbox('2022')


