import os
import time
import requests
import zipfile
import geopandas as gpd
from io import BytesIO

# Define the headers for HTTP requests
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
}

# Define paths based on script's location
script_dir = os.path.dirname(os.path.realpath(__file__))
RAW = os.path.join(script_dir, '..', 'data', 'raw')
PROCESSED = os.path.join(script_dir, '..', 'data', 'processed')

def download_and_save_with_geopandas(url, dest_folder, file_name):
    os.makedirs(dest_folder, exist_ok=True)
    file_path = os.path.join(dest_folder, file_name)
    attempts = 0
    while attempts < 3:  # Retry up to 3 times
        try:
            gdf = gpd.read_file(url)
            gdf.to_file(file_path, driver='GeoJSON')
            return file_path
        except Exception as e:
            print(f"Attempt {attempts+1} failed: {e}")
            attempts += 1
            time.sleep(5)  # Wait for 5 seconds before retrying
    return None



    
def filter_and_save_geojson(file_path, dest_folder, countries):
    gdf = gpd.read_file(file_path)
    gdf.columns = gdf.columns.str.lower()
    for country in countries:
        filtered_gdf = gdf[gdf['country'] == country]
        output_file_name = f"{country.replace(' ', '_').lower()}_country_esri.geojson"
        output_path = os.path.join(dest_folder, output_file_name)
        filtered_gdf.to_file(output_path, driver='GeoJSON')



def download_and_extract_data(url, dest_folder, file_name):
    """Download data handling both direct and zipped GeoJSON files."""
    os.makedirs(dest_folder, exist_ok=True)
    file_path = os.path.join(dest_folder, file_name)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        if url.endswith('.zip'):
            with zipfile.ZipFile(BytesIO(response.content)) as z:
                z.extractall(dest_folder)
                extracted_files = z.namelist()
                if extracted_files:
                    original_path = os.path.join(dest_folder, extracted_files[0])
                    os.rename(original_path, file_path)
        else:
            with open(file_path, 'wb') as f:
                f.write(response.content)
        return file_path
    else:
        print(f"Failed to download data: status code {response.status_code}")
        return None
    


def main():
    # Esri World Countries URL
    WORLD_COUNTRIES_URL = 'https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/World_Countries/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson'
    esri_file_path = download_and_save_with_geopandas(WORLD_COUNTRIES_URL, RAW, 'world_countries_esri.geojson')
    
    if esri_file_path:
        print(f"Downloaded Esri World Countries data successfully.")
        # Filter and save GeoJSON for specific countries
        filter_and_save_geojson(esri_file_path, RAW, ['South Korea', 'North Korea'])

    division_names = {
        0: 'country',
        1: 'province',
        2: 'municipality',
        3: 'district'
    }

    # Country codes to full country names
    country_names = {
        'PRK': 'North Korea',
        'KOR': 'South Korea'
    }

    GADM_URLS = {
        'PRK': [
            'https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_PRK_0.json',
            'https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_PRK_1.json.zip',
            'https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_PRK_2.json.zip'
        ],
        'KOR': [
            'https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_KOR_0.json',
            'https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_KOR_1.json.zip',
            'https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_KOR_2.json.zip',
            'https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_KOR_3.json.zip'
        ]
    }

    for country_code, urls in GADM_URLS.items():
        country_name = country_names[country_code]
        for index, url in enumerate(urls):
            division_name = division_names.get(index, f"level_{index}")
            file_name = f"{country_name.replace(' ', '_').lower()}_{division_name}.geojson"
            gadm_file_path = download_and_extract_data(url, RAW, file_name)
            if gadm_file_path:
                print(f"Downloaded and processed {country_name} {division_name} data.")

if __name__ == "__main__":
    main()