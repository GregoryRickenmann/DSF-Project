###DISCLAIMER###
# The Dataframe used in this file is not to be published

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import chardet

# If we check the data, there are certain letters displayed as �. This is due to the data being encoded in a different way, so we have to find the encoding.
with open("data/export-2024-11-27-08-46-53.csv", "rb") as file:
    result = chardet.detect(file.read())
    print(result['encoding'])

#Now that we have the encoding, we load the file with the detected encoding.
permits = pd.read_csv(
    "data/export-2024-11-27-08-46-53.csv", 
    delimiter=";", 
    encoding="ISO-8859-1")

# Filter rows where BaustKanton is 'SG'
permits = permits[permits['BaustKanton'] == 'SG']

# Further filter rows where BaustPLZ does not start with '9'
filtered_data_no_9 = permits[~permits['BaustPLZ'].astype(str).str.startswith('9')]

# Print the BaustKanton column from the filtered data. We do this to check if they are in St. Gallen
print(filtered_data_no_9['BaustKanton']) # They are, so we keep them

# Here we check if the column "Baustadium" has only 1 value or more.
print(permits['Baustadium'].unique()) # It has only one (Baubewilligung erteilt), so we dont need it

# We check if "BaustadiumAlt" also only has 1 Value.
print(permits['BaustadiumAlt'].unique()) # Here we get different Values, so we keep it.

# We convert BaustadiumDatum and BaustadiumDatumAlt to Datetime
permits['BaustadiumDatum'] = pd.to_datetime(permits['BaustadiumDatum'], errors='coerce')
permits['BaustadiumDatumAlt'] = pd.to_datetime(permits['BaustadiumDatumAlt'], errors='coerce')

print(permits.dtypes)

# Now we only want following columns: Objektname, BaustKanton, BaustadiumDatum, BaustadiumAlt, BaustadiumDatumAlt, Baukosten, Baubeginn, Bauende.
permits = permits[
    ['Objektname', 'BaustKanton', 'BaustadiumDatum', 
     'BaustadiumAlt', 'BaustadiumDatumAlt', 'Baukosten', 'Baubeginn', 'Bauende']
]

# Print the resulting DataFrame
print(permits)

# Identify columns that contain NaN values
nan_columns = permits.columns[permits.isna().any()]

# Loop through each column that contains NaN values
for col in nan_columns:
    # Get the unique values in the column (including NaN) and count the NaNs
    unique_values = permits[col].unique()
    nan_count = permits[col].isna().sum()
    
    # Print the column name, unique values, and the count of NaNs
    print(f"Column: {col}")
    print(f"Unique values (including NaN): {unique_values}")
    print(f"Number of NaN values: {nan_count}\n")

# What we do now is, we transform the columns "Baubeginn", and "Bauende" to 1 (began/ended building) and 0 (didn't begin/end building).
permits['Baubeginn'] = permits['Baubeginn'].notna().astype(int)
permits['Bauende'] = permits['Bauende'].notna().astype(int)

# Print the transformed DataFrame
print(permits)

# Now we try to plot it
# Plot 1: Distribution of Baukosten (Construction Costs)
plt.figure(figsize=(10, 6))
sns.histplot(permits['Baukosten'], kde=True, color='skyblue', bins=20)
plt.title('Distribution of Baukosten (Construction Costs)', fontsize=14)
plt.xlabel('Baukosten (in currency units)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(True)
plt.show()

