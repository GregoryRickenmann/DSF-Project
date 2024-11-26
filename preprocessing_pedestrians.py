import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# There are two datasets for pedestrians, one with data from March 2019 to June 2024 and one with data from June 2024 to Present
pedestrians = pd.read_csv("data/fussganger-stgaller-innenstadt-vadianstrasse-archivdaten.csv", delimiter=";", parse_dates=["datum_tag"])
pedestrians2 = pd.read_csv("data/fussganger-stgaller-innenstadt-vadianstrasse.csv", delimiter=";", parse_dates=["datum_tag"])       

print(pedestrians.sort_values(by="datum_tag", ascending=True))
print(pedestrians2.sort_values(by="datum_tag", ascending=True))

# Some data from the datasets overlaps, so we need to remove some data from one of the datasets, we choose the first one, which is the oldest
pedestrians = pedestrians[pedestrians["datum_tag"] < "2024-06-27"]

# Concatenate both datasets
pedestrians = pd.concat([pedestrians, pedestrians2], axis=0, join="outer", ignore_index=True, verify_integrity=True)

pedestrians = pedestrians.drop(columns=["Sensor ID", "Sensorname", "Gemessen am", "Wochentag", "Standort", "geo_point_2d", "Passanten in Richtung Neumarkt",
       "Passanten in Richtung Multergasse", "device_name"])

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

# Check for NaN values in the dataset
#print(pedestrians.isna().sum())

#print(pedestrians.describe())

days_with_more_than_100_pedestrians = pedestrians[pedestrians["Pedestrians"] > 100]
#print(days_with_more_than_100_pedestrians)


twentyfive = pedestrians["Pedestrians"].quantile(0.25)
seventyfive = pedestrians["Pedestrians"].quantile(0.75)

iquant = seventyfive - twentyfive

outliers = pedestrians[(pedestrians["Pedestrians"] > seventyfive + 1.5 * iquant) | (pedestrians["Pedestrians"] < twentyfive - 1.5 * iquant)]
#print(outliers[outliers["Pedestrians"] > 70])
#print(pedestrians.shape)
