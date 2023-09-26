import pandas as pd

def framework_by_year(df, year):
    d = {'counts': []}
    framework = pd.DataFrame(data=d)

    for col in df.columns:
        frame =df[col].value_counts().reset_index().loc[0]
        framework.loc[frame.iloc[0]] = [frame.iloc[1]]

    framework = framework.reset_index()
    framework = framework[~framework['index'].apply(lambda x: isinstance(x, int))]
    framework = framework[~framework['index'].str.startswith('Which')]
    framework['year'] = year
    framework_counts =framework.sort_values('counts', ascending=False)

    return framework_counts

def framework(df0, df1, df2):
    filter_col = [col for col in df0 if col.startswith('Q16')]
    filter_col.append('year')
    df0= df0[filter_col]

    filter_col = [col for col in df1 if col.startswith('Q16')]
    filter_col.append('year')
    df1= df1[filter_col]

    filter_col = [col for col in df2 if col.startswith('Q17')]
    filter_col.append('year')
    df2 = df2[filter_col]

    framework_2020 = framework_by_year(df0, 2020)
    framework_2021 = framework_by_year(df1, 2021)
    framework_2022 = framework_by_year(df2, 2022)

    merged_df = framework_2022.merge(framework_2021, on='index', how='outer').merge(framework_2020, on='index', how='outer')
    merged_df = merged_df.dropna().drop(columns=['year_x', 'year_y', 'year']).rename(columns={'index':'Framework', 'counts_x':2022, 'counts_y':2021, 'counts':2020})
    merged_df = merged_df.astype(int, errors='ignore')
    merged_df.sort_values(by=2022, ascending=False)
    
    return merged_df.iloc[:5]


