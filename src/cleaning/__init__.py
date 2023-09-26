"""
Author:     Liao Yueh-Fan
Data:       2023/9/21
Course:     NUS IT5006 Fundamentals of Data Analytics
Project:    Job Role Recommendation App
Function:   Init fot Data Cleaning and Preprocessing
"""

from src.cleaning.data_preprecess import data_preprocess

final_data = data_preprocess()
final_data.to_csv(r'..\..\data\processed\Data_Preprocess_v3.csv',
           index=False, header=True, mode='w')