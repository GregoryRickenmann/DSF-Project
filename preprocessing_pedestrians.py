import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# There are two datasets for pedestrians, one with data from March 2019 to June 2024 and one with data from June 2024 to Present
pedestrians = pd.read_csv("data/fussganger-stgaller-innenstadt-vadianstrasse-archivdaten.csv", delimiter=";", parse_dates=["datum_tag"])
pedestrians2 = pd.read_csv("data/fussganger-stgaller-innenstadt-vadianstrasse.csv", delimiter=";", parse_dates=["datum_tag"])       

#print(pedestrians.sort_values(by="datum_tag", ascending=True))
#print(pedestrians2.sort_values(by="datum_tag", ascending=True))

# Some data from the datasets overlaps, so we need to remove some data from one of the datasets, we choose the first one, which is the oldest
pedestrians = pedestrians[pedestrians["datum_tag"] < "2024-06-27"]

# Concatenate both datasets
pedestrians = pd.concat([pedestrians, pedestrians2], axis=0, join="outer", ignore_index=True, verify_integrity=True)

#print(pedestrians.columns)

# Before changing column names to English, drop columns that are not needed
pedestrians = pedestrians.drop(columns=["Sensor ID", "Sensorname", "Gemessen am", "Wochentag", "Standort", "geo_point_2d", "Passanten in Richtung Neumarkt",
       "Passanten in Richtung Multergasse", "device_name"])

# Change column names to English
pedestrians["Date"] = pedestrians["datum_tag"]
pedestrians["Day"] = pedestrians["tag_nr"]
pedestrians["Workday"] = pedestrians["Arbeitstag"]
pedestrians["Pedestrians"] = pedestrians["Passanten in beide Richtungen (Summe)"]
pedestrians = pedestrians.drop(columns=["datum_tag", "tag_nr", "Arbeitstag", "Passanten in beide Richtungen (Summe)"])

# Change Workday to 1 or 0 for True or False
pedestrians["Workday"] = pedestrians["Workday"].apply(lambda x: 1 if x == "Werktage" else 0)

# Check for NaN values in the dataset, there are none
#print(pedestrians.isna().sum())

# Currently "Pedestrians" column is split different time values, so we sum them up to get the total number of pedestrians for one day
daily_pedestrians = pedestrians.groupby('Date')['Pedestrians'].sum().reset_index()

# We then merge the daily_pedestrians with the pedestrians dataset to get the total number of pedestrians for each day
pedestrians = pd.merge(pedestrians, daily_pedestrians, on="Date", how="left")
# Now we drop dates that are duplicates, as we only need one of them, and can also drop the Pedestrians column that is not needed anymore
pedestrians = pedestrians.drop_duplicates(subset=["Date"])
pedestrians.drop(columns=["Pedestrians_x"], inplace=True)

# We then rename the Pedestrians_y column to Total Pedestrians
pedestrians.rename(columns={"Pedestrians_y": "Total Pedestrians"}, inplace=True)

# We examine for errors and outliers in the dataset
#print(pedestrians.describe())

# Plot a boxplot to see outliers
#sns.boxplot(data=pedestrians, y="Total Pedestrians")
#plt.show()

# Thanks to the boxplot we can see that there are no outliers in the dataset

# We can also check that by calculating the interquartile range and checking for values that are more than 1.5 times the interquartile range from the 25th and 75th percentiles
twentyfive = pedestrians["Total Pedestrians"].quantile(0.25)
seventyfive = pedestrians["Total Pedestrians"].quantile(0.75)
iquant = seventyfive - twentyfive
outliers = pedestrians[(pedestrians["Total Pedestrians"] > seventyfive + 1.5 * iquant) | (pedestrians["Total Pedestrians"] < twentyfive - 1.5 * iquant)]
#print(outliers)
#print(outliers.shape)
#print(pedestrians.shape)
#print(f"{outliers.shape[0] / pedestrians.shape[0] * 100:.2f}%")

# So, there are no outliers in the dataset, however, we notice that there are days were there are 0 pedestrians, which is fishy and practically impossible
# We examine those days
days_less_100_pedestrians = pedestrians[pedestrians["Total Pedestrians"] < 100]
#print(days_less_100_pedestrians)

# We notice that only four days have 0 pedestrians, which is not a lot, so we can assume drop these values as they are possibly measurement errors
# We also notice that there is a day with only 1 pedestrian, which is also very unlikely, so we drop this value as well
# Other values can be possible, so we keep them
pedestrians = pedestrians[pedestrians["Total Pedestrians"] > 5]
#print(pedestrians)

# With a histogram we can see how the data is distributed
#sns.histplot(data=pedestrians, x="Total Pedestrians")
#plt.show()

# We notice that the data seems to be normalised, with most values being between 1000 and 3000 pedestrians
# Meaning that our data is not left- or right-skewed

# Data is preprocessed
print(pedestrians)
# Shape 2049 rows with 4 columns (Date, Day, Workday, Total Pedestrians)
