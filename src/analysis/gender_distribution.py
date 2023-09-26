"""
Author:     Chen Bihan
Data:       2023/9/26
Course:     NUS IT5006 Fundamentals of Data Analytics
Project:    Job Role Recommendation App
Function:   Functions for Analysis of gender_distribution
"""
import numpy as np
from src.cleaning import final_data
import matplotlib.pyplot as plt

def plot_gender_distribution(data, years):
    """
    Plot the gender distribution of different country across different years.
    Parameters:
    - data: DataFrame containing the survey data
    - years: List of years to consider for the donut chart
    Returns:
    - A donut chart showing the gender distribution of different country across different years
    """
    # List of developed countries(only use top 5 countries )
    developed_countries = [
        "United States of America", "Japan",
        "United Kingdom of Great Britain and Northern Ireland",
        "France", "Germany"
    ]
    # List of developing countries
    developing_countries = ["India", "Brazil", "China", "Russia", "Indonesia"]
    all_countries = developed_countries + developing_countries
    # Filter data for the specific years and countries
    filtered_data = data[data['year'].astype(str).isin(map(str, years)) & data['Q4_country'].isin(all_countries)]
    # Compute the gender distribution for each country
    gender_counts = filtered_data.groupby(['Q4_country', 'Q3_gender']).size().unstack().fillna(0)
    # Convert gender counts to percentages
    gender_percentage = (gender_counts.divide(gender_counts.sum(axis=1), axis=0) * 100)

    # Mapping for displaying countries in a more concise way
    country_display_names = {
        "United Kingdom of Great Britain and Northern Ireland": "UK",
        "United States of America": "USA"
    }
    # Colors for different genders
    gender_colors = {
        "Man": "#033E6B",
        "Woman": "#A62F00",
        "Prefer not to say": "#FFBF00",
        "Prefer to self-describe": "#F4D35E",
        "Nonbinary": "#83BCA9"
    }
    # List of genders with small percentage values
    small_genders = ["Prefer not to say", "Prefer to self-describe", "Nonbinary"]
    # Create the figure
    plt.figure(figsize=(22, 10))
    # Iterate through each country and plot individual donut chart
    for index, country in enumerate(all_countries):
        plt.subplot(2, 5, index + 1)
        country_data = gender_percentage.loc[country]

        # Function to compute the label for each gender segment in the donut
        def func(pct, allvalues, gender):
            absolute = int(pct / 100. * np.sum(allvalues))
            if gender in small_genders:
                return None
            return f"{pct:.1f}%"

        # Add a slight explosion effect for small percentage genders
        explode = [0.1 if gender in small_genders else 0 for gender in country_data.index]
        # Plot the donut chart
        wedges, texts, autotexts = plt.pie(country_data, labels=None, autopct=lambda pct, allvals=country_data.values,
                                                                                     genderlist=country_data.index: func(
            pct, allvals, genderlist[np.argmax(allvals > pct)]),
                                           startangle=90, wedgeprops=dict(width=0.4),
                                           colors=[gender_colors[gender] for gender in country_data.index],
                                           pctdistance=0.85, explode=explode, textprops=dict(color="w"))

        # Hide the labels for the genders we don't want to show percentage for
        for autotext, gender in zip(autotexts, country_data.index):
            if gender in small_genders:
                autotext.set_text('')
        # Set the title for each individual donut chart
        plt.title(country_display_names.get(country, country))
    # Add a legend
    plt.legend(title="Gender", bbox_to_anchor=(1.15, 0.5), loc="center", labels=gender_percentage.columns)
    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    # Set a dynamic title based on the years
    dynamic_title = f"the gender percentage of different country in {', '.join(map(str, years))}"
    plt.suptitle(dynamic_title, fontsize=18, y=0.98)
    plt.show()

# Just a demonstration since we don't have the data loaded here:
# plot_gender_distribution_individual_donuts_v20(data, [2020, 2021])

plot_gender_distribution(final_data, [2020, 2021,2022])