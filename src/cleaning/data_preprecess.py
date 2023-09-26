"""
Author:     Liao Yueh-Fan
Data:       2023/9/21
Course:     NUS IT5006 Fundamentals of Data Analytics
Project:    Job Role Recommendation App
Function:   Functions for Data Cleaning and Preprocessing
"""
import pandas as pd
import re
import difflib
from src.cleaning import data_preprocess_constant as constant

import os


def data_preprocess():
    # route of the data location
    # 获取当前脚本的绝对路径
    current_path = os.path.abspath(__file__)

    # 获取项目的根目录
    project_root_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))

    loc = project_root_path + "/data/raw/"
    # load data: read question part and answer part separately
    question2020, question2021, question2022, data2020, data2021, data2022 = \
        load_data(loc)
    # try to match questions in different year, output 2021 and 2020 question map
    question2020Mul, question2021Mul, question2022Mul, questionMap2021, questionMap2020 = \
        match_question(question2020, question2021, question2022)
    # rename each data column name to specific format (ex. "Q2_age", "Q13_IDE_Jupyter")
    data2022, data2021, data2020 = \
        col_format(data2020, data2021, data2022, question2020Mul, question2021Mul, question2022Mul,
                   questionMap2021, questionMap2020, constant.dataColNameMap)
    # merge three years data
    data = merge_data(data2020, data2021, data2022)
    # filter student or unemployed answer (only use professional data)
    filter_unprofessional(data)
    # todo: duration time (Get rid of those who take too long or too short time to complete the questionnaire)
    # todo: young age <-> high educational degree
    # todo: age <-> programming / machine learning experience

    return data

def load_data(loc):
    # read kaggle csv data from 2020-2022 (question part)
    question2020 = pd.read_csv(loc + "kaggle_survey_2020_responses.csv", nrows=1)
    question2021 = pd.read_csv(loc + "kaggle_survey_2021_responses.csv", nrows=1)
    question2022 = pd.read_csv(loc + "kaggle_survey_2022_responses.csv", nrows=1)
    # label data with year in the first column
    question2020.insert(0, "year", "2020")
    question2021.insert(0, "year", "2021")
    question2022.insert(0, "year", "2022")
    # rename duration time column name
    question2020.rename(columns={"Time from Start to Finish (seconds)": "Q0"}, inplace=True)
    question2021.rename(columns={"Time from Start to Finish (seconds)": "Q0"}, inplace=True)
    question2022.rename(columns={"Duration (in seconds)": "Q1"}, inplace=True)

    # read kaggle csv data from 2020-2022 (answer part)
    data2020 = pd.read_csv(loc + "kaggle_survey_2020_responses.csv", skiprows=[1])
    data2021 = pd.read_csv(loc + "kaggle_survey_2021_responses.csv", skiprows=[1])
    data2022 = pd.read_csv(loc + "kaggle_survey_2022_responses.csv", skiprows=[1])
    # label data with year in the first column
    data2020.insert(0, "year", "2020")
    data2021.insert(0, "year", "2021")
    data2022.insert(0, "year", "2022")
    # rename duration time column name
    data2020.rename(columns={"Time from Start to Finish (seconds)": "Q0"}, inplace=True)
    data2021.rename(columns={"Time from Start to Finish (seconds)": "Q0"}, inplace=True)
    data2022.rename(columns={"Duration (in seconds)": "Q1"}, inplace=True)

    return question2020, question2021, question2022, data2020, data2021, data2022
def match_question(question2020, question2021, question2022):
    # collect question number contains "_B" (for now we just take _A)
    question2020colB = getColWithStr(question2020, "_B")
    question2021colB = getColWithStr(question2021, "_B")

    # delete question number contains "_B"
    delColWithColName(question2020, question2020colB)
    delColWithColName(question2021, question2021colB)

    # collect question number contains "_" (filter multiple choices questions)
    question2020colMul = getColWithStr(question2020, "_")
    question2021colMul = getColWithStr(question2021, "_")
    question2022colMul = getColWithStr(question2022, "_")
    question2020Mul = pd.DataFrame()
    question2021Mul = pd.DataFrame()
    question2022Mul = pd.DataFrame()

    # pop multiple choices question column to another DataFrame, and rewrite the origin question number/statement
    question2020, question2020Mul = popMulChoiceQuestion(question2020, question2020colMul, question2020Mul)
    question2021, question2021Mul = popMulChoiceQuestion(question2021, question2021colMul, question2021Mul)
    question2022, question2022Mul = popMulChoiceQuestion(question2022, question2022colMul, question2022Mul)

    # match question map for 2021 and 2020 {key=QTitle_2021, value=QTitle_2022}
    questionMap2021 = {}
    questionMap2020 = {}

    # loop all the question in 2022 data and find the most similar question in 2021 data (save in questionMap2021)
    for i in question2022:
        maxRatio = 0
        for j in question2021:
            diffRatio = difflib.SequenceMatcher(a=question2022[i][0].lower(), b=question2021[j][0].lower()).ratio()
            if (maxRatio <= diffRatio and diffRatio > 0.9):
                maxRatio = diffRatio
                questionMap2021[j] = i
    # loop all the question in 2022 data and find the most similar question in 2020 data (save in questionMap2020)
    for i in question2022:
        maxRatio = 0
        for j in question2020:
            diffRatio = difflib.SequenceMatcher(a=question2022[i][0].lower(), b=question2020[j][0].lower()).ratio()
            if (maxRatio <= diffRatio and diffRatio > 0.9):
                maxRatio = diffRatio
                questionMap2020[j] = i

    return question2020Mul, question2021Mul, question2022Mul, questionMap2021, questionMap2020

def delColWithColName(df, colArr):
    # drop specific column name in dataframe (colArr is column name array)
    for col in range(len(colArr)):
        del df[colArr[col]]

def getColWithStr(df, str):
    # go through all the column in dataframe and find column name with 'str' (reutrn columns' name array)
    dfColArr = []
    for col in range(len(df.columns)):
        if str in df.columns.values[col]:
            dfColArr.append(df.columns.values[col])
    return dfColArr

def popMulChoiceQuestion(df, colArr, df_mul):
    # find all the multiple choices question in dataframe and pop to another dataframe(df_mul)
    for col in range(len(colArr)):
        if re.search("_1$", colArr[col]):
            df_mul[colArr[col]] = df[colArr[col]]
            df.update(pd.DataFrame({colArr[col]: [df[colArr[col]][0].split("-", 1)[0].strip()]}))
            df.rename(columns={colArr[col]: colArr[col].split("_", 1)[0]}, inplace=True)
        else:
            df_mul[colArr[col]] = df.pop(colArr[col])
    return df, df_mul
def col_format(data2020, data2021, data2022, question2020Mul, question2021Mul, question2022Mul,
               questionMap2021, questionMap2020, dataColNameMap):
    # rename data 2022 column name to specific format
    for col in data2022:
        if col in dataColNameMap:
            # rename columns name to "Q1_time"
            data2022.rename(columns={col: col + "_" + dataColNameMap[col]}, inplace=True)
        elif "_" in col:
            questionNum = col.split("_", 1)[0]
            shortStatement = dataColNameMap[questionNum]
            choice = question2022Mul[col][0].split("-")[-1].strip()
            # if choice statement contains "(xxxx)" we delete it
            if "(" in choice:
                choice = choice.split("(")[0].strip()
            # update multiple choices question not empty cell value to 1
            data2022[col] = data2022[col].replace(pd.unique(data2022[data2022[col].notnull()][col]), 1)
            # rename columns name to "Q12_coding language_Python"
            data2022.rename(columns={col: questionNum + "_" + shortStatement + "_" + choice}, inplace=True)

    # rename data 2021 column name to specific format
    for col in data2021:
        if "_B" in col:
            continue
        # question find a match (2022 <-> 2021)
        if col in questionMap2021:
            col2022 = questionMap2021[col]
            if col2022 in dataColNameMap:
                # rename columns name to "Q1_time"
                data2021.rename(columns={col: col2022 + "_" + dataColNameMap[col2022]}, inplace=True)
        if "_" in col:
            questionNum = col.split("_", 1)[0]
            if questionNum in questionMap2021:
                questionNum2022 = questionMap2021[questionNum]
                shortStatement = dataColNameMap[questionNum2022]
                choice = question2021Mul[col][0].split("-")[-1].strip()
                if "(" in choice:
                    # if choice statement contains "(xxxx)" we delete it
                    choice = choice.split("(")[0].strip()

                # update multiple choices question not empty cell value to 1
                data2021[col] = data2021[col].replace(pd.unique(data2021[data2021[col].notnull()][col]), 1)
                # rename columns name to "Q12_coding language_Python"
                data2021.rename(columns={col: questionNum2022 + "_" + shortStatement + "_" + choice}, inplace=True)

    # rename data 2020 column name to specific format
    for col in data2020:
        if "_B" in col:
            continue
        # question find a match (2022 <-> 2020)
        if col in questionMap2020:
            col2022 = questionMap2020[col]
            if col2022 in dataColNameMap:
                data2020.rename(columns={col: col2022 + "_" + dataColNameMap[col2022]}, inplace=True)
        if "_" in col:
            questionNum = col.split("_", 1)[0]
            if questionNum in questionMap2020:
                questionNum2022 = questionMap2020[questionNum]
                shortStatement = dataColNameMap[questionNum2022]
                choice = question2020Mul[col][0].split("-")[-1].strip()
                if "(" in choice:
                    choice = choice.split("(")[0].strip()

                # update multiple choices question not empty cell value to 1
                data2020[col] = data2020[col].replace(pd.unique(data2020[data2020[col].notnull()][col]), 1)
                # rename columns name to "Q12_coding language_Python"
                data2020.rename(columns={col: questionNum2022 + "_" + shortStatement + "_" + choice}, inplace=True)

    return data2022, data2021, data2020

def merge_data(data2020, data2021, data2022):
    # merge three years dataset together
    data = pd.concat([data2020, data2021, data2022], ignore_index=True)
    return data

def filter_unprofessional(data):
    # remove students
    data = data[data["Q5_student or not"] != 'No']
    # remove students and currently not employed
    data = data[data["Q23_role title"] != 'Currently not employed']
    data = data[data["Q23_role title"] != 'Student']