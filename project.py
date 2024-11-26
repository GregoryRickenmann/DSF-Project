import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm



df = pd.read_csv('deponieanlieferungen-tufentobel.csv', delimiter=';')

#Check for missing values
missing_values = df.isna().sum()
missing_values

#missing values are in column "Kanton" with only 94 values missing
#also, the there are no relevant outliers in these 94 values
df[df['Kanton'].isna()].describe()

#drop missing values for Kanton
df.dropna(subset=['Kanton'], inplace=True)

#check where the anlieferungen are zero tons
df[df['Gewicht in Tonnen'] == 0].value_counts().sum()

#remove these values
df.drop(df[df['Gewicht in Tonnen'] == 0].index, inplace=True)

#test if it worked
df[df['Gewicht in Tonnen'] == 0].value_counts().sum()

#check very small values
print(df[df['Gewicht in Tonnen'] < 0.1].value_counts().sum())

#check duplicates
duplicates = df.duplicated()
print(f"Number of duplicate rows: {duplicates.sum()}")

#Visualize the outliers in a plot
# plt.figure(figsize=(10, 6))
# plt.boxplot(df['Gewicht in Tonnen'], vert=False)
# plt.title('Boxplot of Gewicht in Tonnen')
# plt.xlabel('Gewicht in Tonnen')
# plt.show()


df[df['Gewicht in Tonnen'] > 35]

#there is one outlier with 56.7 tons, the other values dont go over 35 tons
#remove this outlier
df.drop(df[df['Gewicht in Tonnen'] > 50].index, inplace=True)

# Convert the date column to datetime
df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y')

# Set the date column as the index
df.set_index('Datum', inplace=True)

# Resample the data to monthly frequency, summing the weights
monthly_data = df['Gewicht in Tonnen'].resample('M').sum()

# Perform seasonal decomposition
decomposition = sm.tsa.seasonal_decompose(monthly_data, model='additive')

# Plot the decomposition
fig = decomposition.plot()
fig.set_size_inches(14, 10)
plt.show()
