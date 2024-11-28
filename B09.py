import pandas as pd
import numpy as np

df = pd.DataFrame([2988.826, 3041.892, 3155.796, 2994.507], [2022, 2021, 2020, 2019])

df.rename(columns={0: 'Investments'}, inplace=True)
df.index.name = 'Date'

monthly_weights = {
    "January": 0.07,  # Coldest month, lowest weight
    "February": 0.07,  # Cold month, low weight
    "March": 0.08,
    "April": 0.08,
    "May": 0.085,
    "June": 0.100,  # Hot month, higher weight
    "July": 0.110,  # Hottest month, highest weight
    "August": 0.100,  # Hot month, high weight
    "September": 0.085,
    "October": 0.080,
    "November": 0.07,
    "December": 0.07  # Cold month, lowest weight
}

for month, weight in monthly_weights.items():
    df[month] = df['Investments'] * weight

# Number of days per month (non-leap year)
days_per_month = {
    "January": 31, "February": 28, "March": 31, "April": 30,
    "May": 31, "June": 30, "July": 31, "August": 31,
    "September": 30, "October": 31, "November": 30, "December": 31
}

# Adjust the days for leap years
days_per_month_leap = days_per_month.copy()
days_per_month_leap["February"] = 29  # February has 29 days in leap years
days = [days_per_month, days_per_month, days_per_month_leap, days_per_month]

# Create a date range for all days from 2019 to 2022
date_range = pd.date_range(start='2019-01-01', end='2022-12-31', freq='D')

# Create an empty dataframe with the date range as the index
df_empty = pd.DataFrame(index=date_range)
# Add the 'Investments' column to the empty dataframe
df_empty['Investments'] = np.zeros(len(df_empty))

# Years
for i in range(4):
    # Months
    for j in range(12):
        # Days
        for k in range(list(days[i].items())[j][1]):
            date = f"{2019 + i}-{j + 1}-{k + 1}"
            df_empty.loc[date, 'Investments'] = df.iloc[i][list(days_per_month.items())[j][0]]/list(days[i].items())[j][1]

BO9 = df_empty
print(BO9.head())