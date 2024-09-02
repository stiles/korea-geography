import os
import pandas as pd
import geopandas as gpd

# Define the headers for HTTP requests
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
}

# Absolute paths derived from script's location
script_dir = os.path.dirname(os.path.realpath(__file__))
RAW = os.path.join(script_dir, '..', 'data', 'raw')
PROCESSED = os.path.join(script_dir, '..', 'data', 'processed')

# URL for the data
WORLD_COUNTRIES_URL = 'https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/World_Countries/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson'

countries = ['South Korea', 'North Korea']

def download_data(url, dest_folder, file_name):
    os.makedirs(dest_folder, exist_ok=True)
    file_path = os.path.join(dest_folder, file_name)
    gdf = gpd.read_file(url)
    gdf.to_file(file_path, driver='GeoJSON')
    return file_path

def filter_and_save_geojson(file_path, dest_folder, countries):
    gdf = gpd.read_file(file_path)
    gdf.columns = gdf.columns.str.lower()
    for country in countries:
        filtered_gdf = gdf[gdf['country'] == country]
        output_file_name = f"{country.replace(' ', '_').lower()}.geojson"
        output_path = os.path.join(dest_folder, output_file_name)
        filtered_gdf.to_file(output_path, driver='GeoJSON')

# Download the entire dataset
downloaded_file_path = download_data(WORLD_COUNTRIES_URL, RAW, 'world_countries.geojson')

# If the download was successful, process the file
if downloaded_file_path:
    filter_and_save_geojson(downloaded_file_path, PROCESSED, ['South Korea', 'North Korea'])