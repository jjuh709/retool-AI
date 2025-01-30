import pandas as pd

# Load datasets
location_data = pd.read_csv('data/location_data.csv')
infrastructure_data = pd.read_csv('data/infrastructure_data.csv')
zoning_data = pd.read_csv('data/zoning_data.csv')
amenities_data = pd.read_csv('data/amenities_data.csv')
environmental_data = pd.read_csv('data/environmental_data.csv')
market_data = pd.read_csv('data/market_data.csv')

# Merge datasets
merged_data = pd.merge(location_data, infrastructure_data, on='land_id')
merged_data = pd.merge(merged_data, zoning_data, on='land_id')
merged_data = pd.merge(merged_data, amenities_data, on='land_id')
merged_data = pd.merge(merged_data, environmental_data, on='land_id')
merged_data = pd.merge(merged_data, market_data, on='land_id')

# Feature engineering
city_center_lat, city_center_lon = 34.05, -118.25  # Example coordinates
merged_data['distance_to_city_center'] = ((merged_data['latitude'] - city_center_lat)**2 +
                                          (merged_data['longitude'] - city_center_lon)**2)**0.5
merged_data['soil_quality'] = merged_data['soil_quality'].map({'Poor': 0, 'Fair': 1, 'Good': 2})

# Save merged data
merged_data.to_csv('data/land_price_data.csv', index=False)