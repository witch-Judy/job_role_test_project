"""
Author:     Chen Bihan
Data:       2023/9/26
Course:     NUS IT5006 Fundamentals of Data Analytics
Project:    Job Role Recommendation App
Function:   Functions for Analysis of age vs industry
"""

from src.cleaning import final_data
import seaborn as sns
import matplotlib.pyplot as plt


def plot_age_industry_heatmap(data, years):
    """
    Plot a heatmap showing the distribution of industries based on age groups.

    Parameters:
    - data: DataFrame containing the survey data
    - years: List of years to consider for the heatmap

    Returns:
    - None (Displays the heatmap)
    """
    # Filter data based on the specified years
    filtered_data = data[data['year'].astype(str).isin(map(str, years))]

    # Compute the count of respondents in each industry for each age group
    industry_age_counts = filtered_data.groupby(['Q2_age', 'Q24_industry']).size().unstack().fillna(0)

    # Normalize the counts to get percentages
    industry_age_percentage = industry_age_counts.divide(industry_age_counts.sum(axis=1), axis=0)

    # Plotting
    plt.figure(figsize=(15, 10))
    sns.heatmap(industry_age_percentage, cmap="vlag", annot=True, fmt=".2%", cbar_kws={'label': 'Percentage'})

    plt.title(f"Industry Distribution Based on Age Groups for Years {', '.join(map(str, years))}", fontsize=16)
    plt.xlabel("Industry", fontsize=14)
    plt.ylabel("Age Group", fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# For demonstration, plot the heatmap for the years 2020 and 2021
plot_age_industry_heatmap(final_data, [2020, 2021, 2023])

