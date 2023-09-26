import pandas as pd

def title(df0, df1, df2):
    filter_col = [col for col in df0 if col.startswith('Q5')]
    filter_col.append('year')
    df0= df0[filter_col].drop(0)

    filter_col = [col for col in df1 if col.startswith('Q5')]
    filter_col.append('year')
    df1= df1[filter_col].drop(0)

    filter_col = [col for col in df2 if col.startswith('Q5')]
    filter_col.append('year')
    df2_students = df2[filter_col].drop(0)

    filter_col = [col for col in df2 if col.startswith('Q23')]
    filter_col.append('year')
    df2 = df2[filter_col].drop(0)

    no_of_stu = df2_students.value_counts().iloc[1]
    df2 = df2.value_counts().reset_index().rename(columns={'Q23':'title'})

    new_row = {'title': 'Student', 'year': 2022, 'count':no_of_stu}
    df2.loc[-1] = new_row
    df2.index = df2.index + 1
    df2 = df2.sort_index()

    df2.at[2, 'title'] = 'Data Analyst'
    df0 = df0.value_counts().reset_index().rename(columns={'Q5':'title'})
    df1 = df1.value_counts().reset_index().rename(columns={'Q5':'title'})
    merged_df = df2.merge(df1, on='title', how='outer').merge(df0, on='title', how='outer')

    top5=merged_df.dropna().iloc[:5]
    top5 = top5.drop(columns=['year_x', 'year_y', 'year']).rename(columns={'count_x':2022, 'count_y':2021, 'count':2020})
    top5df = top5.astype(int, errors='ignore')

    return top5df