import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

weather = pd.read_csv("data/wetterdaten-klimamessnetz-kanton-stgallen-tageswerte.csv", delimiter=";", parse_dates=["Datum"])

# Change column names to English
weather["Location"] = weather["Station/Location"]
weather["Date"] = weather["Datum"]
weather["Temperature mean"] = weather["Lufttemperatur 2 m über Boden; Tagesmittel"]
weather["Temperature max"] = weather["Lufttemperatur 2 m über Boden; Tagesmaximum"]
weather["Temperature min"] = weather["Lufttemperatur 2 m über Boden; Tagesminimum"]
weather["Precipitation in mm"] = weather["Niederschlag; Tagessumme 6 UTC - 6 UTC Folgetag"]
weather["Snow amount in cm"] = weather["Gesamtschneehöhe; Morgenmessung von 6 UTC"]
weather = weather.drop(columns=["Station/Location", "Datum", "Lufttemperatur 2 m über Boden; Tagesmittel", "Lufttemperatur 2 m über Boden; Tagesmaximum", "Lufttemperatur 2 m über Boden; Tagesminimum", "Niederschlag; Tagessumme 6 UTC - 6 UTC Folgetag", "Gesamtschneehöhe; Morgenmessung von 6 UTC"])

# Check for unique locations
#print(weather['Station/Location'].unique())

# Only use data from St. Gallen, drop all other stations (Bad Ragaz and Säntis)
# Also drop columns that are not needed, for instance, Globalstrahtlung, Gesamtbewölkung, Luftdruck, Luftfeuchtigkeit and Sonnenscheindauer
weather = weather[weather["Location"] == "St. Gallen"]
weather = weather.drop(columns=["Globalstrahlung; Tagesmittel", "Gesamtbewölkung; Tagesmittel", "Luftdruck auf Stationshöhe (QFE); Tagesmittel", "Relative Luftfeuchtigkeit 2 m über Boden; Tagesmittel", "Sonnenscheindauer; Tagessumme"])

# Make sure that only the St. Gallen station is left
#print(weather['Station/Location'].unique())

# We only need data from 2019 onwards since the trash dataset starts on January 3rd, 2019
weather = weather[weather["Date"] >= "2019-01-01"] 

# Check for NaN values in the dataset
#print(weather.isna().sum())

# Check for duplicates
#print(weather.duplicated().sum())

# There are no NaN values or duplicates in the dataset left
print(weather.head())
