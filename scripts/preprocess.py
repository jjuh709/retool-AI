import pandas as pd
import os

# Correct file path for environmental data
file_path = '/workspaces/retool-AI/data/environmental_data.csv'

# Check if file exists and is readable
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {os.path.abspath(file_path)}")
if not os.access(file_path, os.R_OK):
    raise PermissionError(f"Cannot read file: {os.path.abspath(file_path)}")

# Load environmental data with error handling
try:
    environmental_data = pd.read_csv(file_path)
    if environmental_data.empty:
        raise ValueError("The file is empty.")
except pd.errors.EmptyDataError:
    raise ValueError("The file is empty or improperly formatted.")
except Exception as e:
    raise RuntimeError(f"An unexpected error occurred while loading the file: {e}")

# Debugging: Print environmental data columns
print("Environmental data columns:", environmental_data.columns)

# Load other datasets
datasets = ['location_data', 'infrastructure_data', 'zoning_data', 'amenities_data', 'market_data']
dataframes = {}

# Load datasets dynamically
for dataset in datasets:
    path = f"/workspaces/retool-AI/data/{dataset}.csv"
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {os.path.abspath(path)}")
    dataframes[dataset] = pd.read_csv(path)

# Rename soil_quality to avoid conflicts
environmental_data = environmental_data.rename(columns={'soil_quality': 'env_soil_quality'})

# Merge datasets on 'land_id'
merged_data = dataframes['location_data']
for dataset in datasets[1:]:
    merged_data = pd.merge(merged_data, dataframes[dataset], on='land_id')

# Add environmental data
merged_data = pd.merge(merged_data, environmental_data, on='land_id')

# Debugging: Print merged columns
print("Merged data columns:", merged_data.columns)

# Feature engineering
city_center_lat, city_center_lon = 34.05, -118.25  # Example coordinates
merged_data['distance_to_city_center'] = ((merged_data['latitude'] - city_center_lat)**2 +
                                          (merged_data['longitude'] - city_center_lon)**2)**0.5
merged_data['env_soil_quality'] = merged_data['env_soil_quality'].map({'Poor': 0, 'Fair': 1, 'Good': 2})

# Save merged data
output_path = '/workspaces/retool-AI/data/land_price_data.csv'
merged_data.to_csv(output_path, index=False)
print(f"Merged data saved to {os.path.abspath(output_path)}")
