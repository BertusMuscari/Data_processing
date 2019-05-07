import pandas as pd

# Read csv into dataframe
df = pd.read_csv("input.csv", decimal=",")
df = df.loc[df['TIME'] == 2017]
df = df.loc[df['SUBJECT'] == "DTP"]
df1 = df[['LOCATION','VALUE']]
# Transform to Json
df1.to_json('output.json', orient='records')
