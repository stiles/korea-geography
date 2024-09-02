import os
import glob

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

# Paths to the directories containing the files
english_dir = 'data/raw/ngii/english'
korean_dir = 'data/raw/ngii/korean'

# Pattern and dictionary setup
pattern = '*.*'

# Call rename_files and clean_up_old_files
english_renamed_files = rename_files(english_dir, pattern, rename_dict)
korean_renamed_files = rename_files(korean_dir, pattern, rename_dict)

# Cleanup old files
clean_up_old_files(english_dir, english_renamed_files)
clean_up_old_files(korean_dir, korean_renamed_files)