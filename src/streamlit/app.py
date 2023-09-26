"""
Author:     Chen Bihan
Data:       2023/9/26
Course:     NUS IT5006 Fundamentals of Data Analytics
Project:    Job Role Recommendation App
Function:   Functions for app
"""

import streamlit as st
from src.cleaning import final_data
from src.analysis.coding_language_country import plot_language_trend

# Sidebar title
st.sidebar.title("Job Role Recommendation")

# Main categories: Data Analysis and Recommendation
main_selection = st.sidebar.selectbox("Choose a category", ["Data Analysis", "Recommendation system"])

# If Data Analysis is selected
if main_selection == "Data Analysis":
    st.write("## Data Analysis")

    # Sub-categories for Data Analysis: x class and y class
    analysis_selection = st.sidebar.selectbox("Choose a class", ["<x>", "<y>"])

    # If x class is selected under Data Analysis
    if analysis_selection == "<x>":
        st.write("### <x> Analysis")

        # Add sub-titles for x class
        x_sub_title = st.sidebar.selectbox("Choose a sub-title for x class", ["country_income", "Machine learning framework", "coding_language"])
        st.write(f"You chose {x_sub_title} under {analysis_selection}")

        # If 'coding_language' is selected, add a country selector and display the plot based on the selected country
        if x_sub_title == "coding_language":
            # Add a country selector
            country = st.sidebar.selectbox("Choose a country", ["United States of America", "Japan", "India", "China", "Germany", "France", "Brazil", "Russia", "United Kingdom", "Indonesia"])
            # Display the plot based on the selected country
            plot_language_trend(final_data, country)
            st.write("## crazy")



    # If y class is selected under Data Analysis
    elif analysis_selection == "<y>":
        st.write("### <y> Analysis")

        # Add sub-titles for y class
        y_sub_title = st.sidebar.selectbox("Choose a sub-title for y class", ["Programming experience vs Salary", "income_country", "the composition of industry based on age","job_title","the gender ratio"])
        st.write(f"You chose {y_sub_title} under {analysis_selection}")
        # Display content or analysis for the chosen sub-title

# If Recommendation is selected
elif main_selection == "Recommendation":
    st.write("## Recommendation")

# Remember to run the app with: streamlit run your_script_name.py
