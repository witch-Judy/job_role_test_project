import pandas as pd

def country_income(df0, df1, df2, year, country):
    a=df0[['Q3','Q24']].copy()
    a.rename(columns={'Q3': 'Country', 'Q24':'Yearly_compensation'},inplace=True)
    b=df1[['Q3','Q25']].copy()
    b.rename(columns={'Q3': 'Country', 'Q25':'Yearly_compensation'},inplace=True)
    c=df2[['Q4','Q29']].copy()
    c.rename(columns={'Q4': 'Country', 'Q29':'Yearly_compensation'},inplace=True)
    
    df_country_income = pd.concat([a[1:],b[1:],c[1:]])
    a = df_country_income['Yearly_compensation']
    b = a.str.split('-', expand=True)[1]
    b = b.str.replace(',', '')
    df_country_income['Yearly_compensation'] = b

    # find by country
    ls = df_country_income['Country'] == country
    income_of_country = df_country_income[ls]
    data = income_of_country['Yearly_compensation']
    data = data.astype(float)

    return data