import pandas as pd

#Loading data
df = pd.read_csv(r'C:\Users\Fernando\pyproj\my_env\Fran_WeeklySheet_20240506.xls.csv')

print(df.head(), df.dtypes, df.shape)

# Remove duplicate rows if any and checking how many rows were duplicates
data_cleaned = df.drop_duplicates()

# Check how many rows were duplicates
duplicates_removed = df.shape[0] - data_cleaned.shape[0]

print(duplicates_removed, data_cleaned.shape)

#Removing irrelevant columns for project - Considering the questions we are trying to answer
columns_to_remove = ['Sales ID', 'Agent ID (From Client)', 'Package (From Client)', 'Notes', 'Store Name', 'Store ID']

data_cleaned = data_cleaned.drop(columns=columns_to_remove)

print(data_cleaned.shape)

# Creating address, zip code and state columns for analysis that will be conducted later
# Display unique address entries to confirm their format
data_cleaned['Address'].unique()


# Function to extract city, state, and zipcode from an address string
def extract_address_components(address):
    if pd.isna(address):
        return pd.Series(['Unknown', 'Unknown', 'Unknown'])
    try:
        # Extracting parts assuming format "Street, City, State ZIP"
        parts = address.rsplit(', ', maxsplit=2)
        if len(parts) == 3:  # Ideal case "Street, City, State ZIP"
            street, city, state_zip = parts
        elif len(parts) == 2:  # No comma between city and state "Street City, State ZIP"
            street, city_state_zip = parts
            city, state_zip = city_state_zip.rsplit(' ', 1)
        else:
            street = parts[0]
            city, state_zip = street.rsplit(' ', 1)

        state, zipcode = state_zip.rsplit(' ', 1)
    except ValueError:  # In case any error in splitting due to unexpected format
        city, state, zipcode = 'Unknown', 'Unknown', 'Unknown'

    return pd.Series([city, state, zipcode])


# Applying the function to the Address column and create new columns
data_cleaned[['City', 'State', 'Zipcode']] = data_cleaned['Address'].apply(extract_address_components)
print(data_cleaned[['City', 'State', 'Zipcode', 'Address']].head())


# Cleaning new columns in case we have inconsistencies

def clean_text(text):
    if pd.isna(text):
        return "Unknown"
    # Strip whitespace and capitalize properly for cities
    return text.strip().title()

def clean_state(state):
    if pd.isna(state):
        return "Unknown"
    # Ensure state codes are upper case
    return state.strip().upper()

def clean_zipcode(zipcode):
    if pd.isna(zipcode) or not zipcode.isdigit() or len(zipcode) != 5:
        return "Unknown"
    return zipcode.strip()

# Apply cleaning functions
data_cleaned['City'] = data_cleaned['City'].apply(clean_text)
data_cleaned['State'] = data_cleaned['State'].apply(clean_state)
data_cleaned['Zipcode'] = data_cleaned['Zipcode'].apply(clean_zipcode)

# Checking the cleaned columns
print(data_cleaned[['City', 'State', 'Zipcode']].head())

print(data_cleaned.head())

# Noticed some dtypes I want to change so will change them
print(data_cleaned.dtypes)
# Changing fields that are unique identifiers to strings
identifier_columns = ['ID', 'Work Order Number', 'Account Number', 'Mobile Order Number', 'TPV Confirmation Number', 'Process Status']
data_cleaned[identifier_columns] = data_cleaned[identifier_columns].astype(str)

# Verifying the changes to data types
print(data_cleaned.dtypes)

data = data_cleaned

print(data_cleaned.shape)

# I noticed some columns had NaN and some had an actual string containing 'nan' so I need to clean those
# Defining the columns to check for NaN or 'nan' string and checking them
columns_to_check = ['ID', 'Work Order Number', 'TPV Confirmation Number', 'Process Status']
condition = data[columns_to_check].apply(lambda col: col.isna() | col.map(lambda x: x == 'nan')).all(axis=1)

# Filter the DataFrame to exclude rows that meet the condition (where all specified columns are NaN or 'nan') and checking the data
cleaned_nan_data = data[~condition]
print(cleaned_nan_data.shape)
print(cleaned_nan_data.head(20))

#noticed I need to standardize some agent names
# Using .loc to ensure I am modifying the DataFrame view directly
cleaned_nan_data.loc[:, 'Agent Name'] = cleaned_nan_data['Agent Name'].str.title()

print(cleaned_nan_data.head(10))

# Data looks clean now for the kind of analysis we will be conducting

#Saving the cleaned DataFrame to a new CSV file
cleaned_nan_data.to_csv('cleaned_ascent5sales.csv',index=False)