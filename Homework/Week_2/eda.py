#!/usr/bin/env python
# Name: Machiel Cligge
# Student number: 10772006
"""
This script explores data for infant mortality, population density and gdp for countries.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import datafile as panda DataFrame
df = pd.read_csv("input.csv", decimal=",", index_col="Country", na_values="unknown")

# Make column titles easier
gdp = 'GDP ($ per capita) dollars'
pop = 'Pop. Density (per sq. mi.)'
mort = 'Infant mortality (per 1000 births)'

# Clean dataframe
df[gdp] = df[gdp].str.strip(' dollars')
df[gdp] = pd.to_numeric(df[gdp], errors='coerce')
df['Region'] = df['Region'].str.strip()

def remove_outliers(column_name):
    """
    Removes outliers from data if outside of boxplot whiskers
    """
    q1 = df[column_name].quantile(0.25)
    q3 = df[column_name].quantile(0.75)
    iqr = q3 - q1
    whisker_low  = q1 - 1.5 * iqr
    whisker_high = q3 + 1.5 * iqr
    new_df = df[column_name][df[column_name].between(whisker_low, whisker_high)]
    return new_df

# Convert to Json

if __name__ == "__main__":
    # Remove outliers from data
    df[gdp] = remove_outliers(gdp)
    df[pop] = remove_outliers(pop)
    df[mort] = remove_outliers(mort)

    # Central tendency
    print(f"Mean GDP: {df[gdp].mean()}\n" +
          f"Median GDP: {df[gdp].median()}\n" +
          f"Mode GDP: {df[gdp].mode()}")

    df.hist(gdp, grid=False)
    plt.show()

    # Five number summary of infant mortality
    des = df[mort].describe(percentiles=[.25, .50, .75])
    print(f"Minimum infant mortality (per 1000 births): {des['min']}\n" +
          f"First quartile: {des['25%']}\n" +
          f"Second quartile: {des['50%']}\n" +
          f"Third quartile: {des['75%']}\n" +
          f"Maximum infant mortality (per 1000 births): {des['max']}")

    df.boxplot(mort)
    plt.show()

    # Make Json file
    df[['Region', 'Pop. Density (per sq. mi.)', 'GDP ($ per capita) dollars', 'Infant mortality (per 1000 births)']].to_json('output.json', orient='index')
