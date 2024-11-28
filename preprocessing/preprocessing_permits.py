###DISCLAIMER###
# The Dataframe used in this file is not to be published
# All copyrights belong to Infopro Digital Schweiz GmbH

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import chardet

# If we check the data, there are certain letters displayed as �. This is due to the data being encoded in a different way, so we have to find the encoding
with open("data/export-2024-11-27-08-46-53.csv", "rb") as file:
    result = chardet.detect(file.read())
    print(result['encoding'])

#Now that we have the encoding, we load the file with the detected encoding
permits = pd.read_csv(
    "data/export-2024-11-27-08-46-53.csv", 
    delimiter=";", 
    encoding="ISO-8859-1")

# Filter rows where BaustKanton is 'SG'
permits = permits[permits['BaustKanton'] == 'SG']

# Further filter rows where BaustPLZ does not start with '9'
filtered_data_no_9 = permits[~permits['BaustPLZ'].astype(str).str.startswith('9')]

# Print the BaustKanton column from the filtered data. We do this to check if they are in St. Gallen
filtered_data_no_9['BaustKanton'] # They are, so we keep them

# Here we check if the column "Baustadium" has only 1 value or more
permits['Baustadium'].unique() # It has only one (Baubewilligung erteilt), so we dont need it

# We check if "BaustadiumAlt" also only has 1 Value
permits['BaustadiumAlt'].unique() # Here we get different Values, so we keep it

# Check the first few rows of 'BaustadiumDatum' and 'BaustadiumDatumAlt' for format
permits[['BaustadiumDatum', 'BaustadiumDatumAlt']].head() # There are certain Values in the Dataframe that are like "Aug 2024". If we wanted to convert this to datetime it would output NaT

# Here we fix the Problem of the different time notations
# Function to handle the transformation of month-year to day-month-year and convert to datetime
def fix_and_convert_dates(date_column):
    # Step 1: Convert month-year format (e.g. "Aug 2024") to "01-Aug-2024"
    # Replace entries like 'Aug 2024' with '01-Aug-2024'
    date_column = date_column.str.replace(r'([A-Za-z]+ \d{4})', r'01-\1', regex=True)
    
    # Step 2: Convert all dates (including the modified ones) to datetime
    # Try converting to datetime using day-first format (for d.m.Y format like '15.08.2024')
    return pd.to_datetime(date_column, errors='coerce', dayfirst=True)

# Apply the function to both columns
permits['BaustadiumDatum'] = fix_and_convert_dates(permits['BaustadiumDatum'])
permits['BaustadiumDatumAlt'] = fix_and_convert_dates(permits['BaustadiumDatumAlt'])

# Check the results
print(permits[['BaustadiumDatum', 'BaustadiumDatumAlt']].head())

# Check for NaT in datetime columns
permits['BaustadiumDatum'].isna().sum()  # Sum of NaT values in the 'BaustadiumDatum' column

permits['BaustadiumDatumAlt'].isna().sum()  # Sum of NaT values in the 'BaustadiumDatumAlt' column

permits.dtypes

# Now we only want following columns: BaustadiumDatum and Baukosten
permits = permits[
    ['BaustadiumDatum', 'Baukosten']
]

# We notice that 'Baukosten' is an object, so we need to convert it to a float
# First we need to remove the ' characters
permits['Baukosten'] = permits['Baukosten'].str.replace("'", "")

# Now we need to remove the 'Mio CHF'
permits['Baukosten'] = permits['Baukosten'].str.replace("Mio CHF", "")

# For values that have a bandwith, we take the average
# For values that are not numbers, we convert them to NaN
def convert_baukosten(value):
    try:
        if "-" in value:
            value = value.split("-")
            return (float(value[0]) + float(value[1])) / 2
        else:
            return float(value)
    except ValueError:
        return np.nan

# Apply the function to the 'Baukosten' column
permits['Baukosten'] = permits['Baukosten'].apply(convert_baukosten)

# Check how many NaN values are in the 'Baukosten' column
permits['Baukosten'].isna().sum()

# Drop rows with NaN values in 'Baukosten' column
permits = permits.dropna(subset=['Baukosten'])

# Check the data types of the columns
permits.dtypes

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

permits["Date"] = permits["BaustadiumDatum"]
permits.drop(columns=["BaustadiumDatum"], inplace=True)

# We notice that there are 1421 duplicates
# For these values, we sum all the Baukosten values to get the total cost for that day
daily_costs = permits.groupby('Date')['Baukosten'].sum().reset_index()

# We then merge the daily_costs with the permits dataset to get the total costs for each day
permits = pd.merge(permits, daily_costs, on="Date", how="left")
# Now we drop dates that are duplicates, as we only need one of them, and can also drop the Baukosten column that is not needed anymore
permits = permits.drop_duplicates(subset=["Date"])
permits.drop(columns=["Baukosten_x"], inplace=True)

# We then rename the Baukosten_y column to Total Costs
permits.rename(columns={"Baukosten_y": "Total Costs"}, inplace=True)

permits.describe()

# We check for outliers with a boxplot
sns.boxplot(data=permits, x='Total Costs')
plt.show()

# We notice that there are some outliers, but they might be relevant since it's possible that some construction projects are more expensive than others
# Furthermore, it is also possible that on some days, there are more construction projects being permitted than on others, which would lead to higher costs

# The data has been preprocessed
PERMITS = permits
