import os
import time
import glob
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

RAW_ESRI = os.path.join(RAW, 'esri')
RAW_GADM = os.path.join(RAW, 'gadm')
RAW_NGII = os.path.join(RAW, 'ngii')

# Paths to the directories containing the files
ENG_DIR = 'data/raw/ngii/english'
KOR_DIR = 'data/raw/ngii/korean'

# Pattern and dictionary setup
pattern = '*.*'

# Dictionary for renaming the files
rename_dict = {
    '23│Γ ┤δ╟╤╣╬▒╣└ⁿ╡╡(120╕╕-┐╡╣«) ║»╚¡┴÷┐¬ ║±▒│╟Ñ': 'South Korea Map Comparison of Changing Areas at 1:1,200,000 Scale in Korean (23rd Year)',
    'KOR_ADMIN_AS_┐╡╣«': 'administrative_boundaries_english',
    'KOR_COAST_LS_┐╡╣«': 'coastal_lines_english',
    'KOR_CULTU_PS_┐╡╣«': 'cultural_locations_english',
    'KOR_DZONE_LS_┐╡╣«': 'demilitarized_zone_english',
    'KOR_LATLO_LS_┐╡╣«': 'latitude_longitude_lines_english',
    'KOR_MOUNT_PS_┐╡╣«': 'mountain_peaks_english',
    'KOR_NAION_AS_┐╡╣«': 'national_boundaries_english',
    'KOR_NAME_PS_┐╡╣«': 'place_names_english',
    'KOR_OCEAN_PS_┐╡╣«': 'ocean_points_english',
    'KOR_PREMI_PS_┐╡╣«': 'premier_points_english',
    'KOR_RAILW_LS_┐╡╣«': 'railways_english',
    'KOR_RIVER_LS_┐╡╣«': 'rivers_english',
    'KOR_ROAD_LS_┐╡╣«': 'roads_english',
    # Korean names, adapt these if actual names are slightly different
    '23│Γ ┤δ╟╤╣╬▒╣└ⁿ╡╡(120╕╕-▒╣╣«) ║»╚¡┴÷┐¬ ║±▒│╟Ñ': 'South Korea Map Comparison of Changing Areas at 1:1,200,000 Scale in Korean (23rd Year)',
    'KOR_ADMIN_AS_▒╣╣«': 'administrative_boundaries_korean',
    'KOR_COAST_LS_▒╣╣«': 'coastal_lines_korean',
    'KOR_CULTU_PS_▒╣╣«': 'cultural_locations_korean',
    'KOR_DZONE_LS_▒╣╣«': 'demilitarized_zone_korean',
    'KOR_LATLO_LS_▒╣╣«': 'latitude_longitude_lines_korean',
    'KOR_MOUNT_PS_▒╣╣«': 'mountain_peaks_korean',
    'KOR_NAION_AS_▒╣╣«': 'national_boundaries_korean',
    'KOR_NAME_PS_▒╣╣«': 'place_names_korean',
    'KOR_OCEAN_PS_▒╣╣«': 'ocean_points_korean',
    'KOR_PREMI_PS_▒╣╣«': 'premier_points_korean',
    'KOR_RAILW_LS_▒╣╣«': 'railways_korean',
    'KOR_RIVER_LS_▒╣╣«': 'rivers_korean',
    'KOR_ROAD_LS_▒╣╣«': 'roads_korean'
}

def download_geojson_and_save(url, dest_folder, file_name):
    """Download GeoJSON directly into GeoPandas and save locally."""
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

def download_and_extract_archive(url, dest_folder, file_name):
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

def download_and_extract_ngii_data(url, dest_folder):
    """Download and extract NGII data, which may contain multiple files."""
    os.makedirs(dest_folder, exist_ok=True)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content)) as z:
            z.extractall(dest_folder)
        print(f"Downloaded and extracted files to {dest_folder}")
    else:
        print(f"Failed to download NGII data: status code {response.status_code}")

def filter_and_save_geojson(file_path, dest_folder, countries):
    gdf = gpd.read_file(file_path)
    gdf.columns = gdf.columns.str.lower()
    for country in countries:
        filtered_gdf = gdf[gdf['country'] == country]
        output_file_name = f"{country.replace(' ', '_').lower()}_country_esri.geojson"
        output_path = os.path.join(dest_folder, output_file_name)
        filtered_gdf.to_file(output_path, driver='GeoJSON')

def rename_files(directory, pattern, rename_dict):
    files = glob.glob(os.path.join(directory, pattern))
    renamed_files = []  # List to store names of successfully renamed files
    for file_path in files:
        base_name = os.path.basename(file_path)
        name_part, ext = os.path.splitext(base_name)
        if name_part in rename_dict:
            new_name = rename_dict[name_part] + ext
            new_path = os.path.join(directory, new_name)
            os.rename(file_path, new_path)
            renamed_files.append(new_name)
            print(f'Renamed {file_path} to {new_path}')
        else:
            print(f'No entry for {name_part} in dictionary')
    return renamed_files

def clean_up_old_files(directory, keep_files):
    for filename in os.listdir(directory):
        if filename not in keep_files:
            file_path = os.path.join(directory, filename)
            try:
                os.remove(file_path)
                print(f"Removed old file: {filename}")
            except Exception as e:
                print(f"Failed to remove {filename}: {e}")

def main():
    # Setup directories
    for dir_path in [RAW_ESRI, RAW_GADM, RAW_NGII, PROCESSED]:
        os.makedirs(dir_path, exist_ok=True)

    # Download and process Esri World Countries
    WORLD_COUNTRIES_URL = 'https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/World_Countries/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson'
    esri_file_path = download_geojson_and_save(WORLD_COUNTRIES_URL, RAW, 'world_countries_esri.geojson')
    
    if esri_file_path:
        print(f"Downloaded Esri World Countries data successfully.")
        # Filter and save GeoJSON for specific countries
        filter_and_save_geojson(esri_file_path, RAW_ESRI, ['South Korea', 'North Korea'])

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
            gadm_file_path = download_and_extract_archive(url, RAW_GADM, file_name)
            if gadm_file_path:
                print(f"Downloaded and processed {country_name} {division_name} data.")

    # Download NGII data
    NGII_URLS = {
        "English": "https://www.ngii.go.kr/other/file_down.do?sq=107989",
        "Korean": "https://www.ngii.go.kr/other/file_down.do?sq=107985"
    }
    for language, url in NGII_URLS.items():
        ngii_dest_folder = os.path.join(RAW_NGII, language.lower())
        download_and_extract_ngii_data(url, ngii_dest_folder)

    # Call rename_files and clean_up_old_files
    english_renamed_files = rename_files(ENG_DIR, pattern, rename_dict)
    korean_renamed_files = rename_files(KOR_DIR, pattern, rename_dict)

    # Cleanup old files
    clean_up_old_files(ENG_DIR, english_renamed_files)
    clean_up_old_files(KOR_DIR, korean_renamed_files)

if __name__ == "__main__":
    main()