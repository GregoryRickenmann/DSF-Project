import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from preprocessing_weather import WEATHER
from preprocessing_pedestrians import PEDESTRIANS
from BO9 import BO9
from preprocessing_permits import PERMITS

df = pd.read_csv("data/deponieanlieferungen-tufentobel.csv", delimiter=';')
#preprocessing of df (tüfentobel)

#Check for missing values
missing_values = df.isna().sum()
# missing_values

#missing values are in column "Kanton" with only 94 values missing
#also, the there are no relevant outliers in these 94 values
# df[df['Kanton'].isna()].describe()

#drop missing values for Kanton
df.dropna(subset=['Kanton'], inplace=True)

#check where the anlieferungen are zero tons
df[df['Gewicht in Tonnen'] == 0].value_counts().sum()

#remove these values
df.drop(df[df['Gewicht in Tonnen'] == 0].index, inplace=True)

#test if it worked
df[df['Gewicht in Tonnen'] == 0].value_counts().sum()

#check very small values
#print(df[df['Gewicht in Tonnen'] < 0.1].value_counts().sum())

#check duplicates
duplicates = df.duplicated()
#print(f"Number of duplicate rows: {duplicates.sum()}")

# #Visualize the outliers in a plot
# plt.figure(figsize=(10, 6))
# plt.boxplot(df['Gewicht in Tonnen'], vert=False)
# plt.title('Boxplot of Gewicht in Tonnen')
# plt.xlabel('Gewicht in Tonnen')
# plt.show()

# df[df['Gewicht in Tonnen'] > 35]

#there is one outlier with 56.7 tons, the other values dont go over 35 tons
#remove this outlier
df.drop(df[df['Gewicht in Tonnen'] > 50].index, inplace=True)

# Convert the date column to datetime and ensure the format is year, month, day

# Only keep columns that are relevant for the analysis
df = df[["Anlieferungsdatum", "Material", "Gewicht in Tonnen"]]
# Convert the Anlieferungsdatum column to datetime and remove the time part
df['Anlieferungsdatum'] = pd.to_datetime(df['Anlieferungsdatum'], utc=True)
#df['Anlieferungsdatum'] = pd.to_datetime(df['Anlieferungsdatum'], errors='coerce').dt.date
df['Anlieferungsdatum'] = df['Anlieferungsdatum'].dt.tz_localize(None).dt.date
df['Anlieferungsdatum'] = pd.to_datetime(df['Anlieferungsdatum'])

# merge the features pedestrians and weather with the df
merged_features = pd.merge(PEDESTRIANS, WEATHER, on='Date', how='inner')

features = pd.merge(df, merged_features, left_on='Anlieferungsdatum', right_on="Date", how='inner')

# Drop Date column since there is already a Anlieferungsdatum which tells the date
features.drop(columns=['Date'], inplace=True)

new_features = pd.merge(features, PERMITS, left_on='Anlieferungsdatum', right_on='Date', how='left')
new_features.drop(columns=['Date'], inplace=True)

# Replaces NaN values with 0 
new_features.replace(np.nan, 0, inplace=True)
NEW_FEATURES = new_features