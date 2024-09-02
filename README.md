# Korean geography
Scripts for downloading, processing and storing spatial data for North and South Korea.

## Process

### Script functionality
The repo relies on a Python script — `scripts/fetch.py` — to fetch data for country boundaries and administrative divisions and rename some files so they're in English and more descriptive. The script uses a `main()` function to orchestrate these downloading and processing tasks.  

#### Data sources:
- [Esri world countries](https://hub.arcgis.com/datasets/esri::world-countries/explore?location=-0.035893%2C0.000000%2C2.01): The script downloads and saves the data from an Esri endpoint, splitting out national boundary files for North and South Korea. 

- [Database of Global Administrative Areas](https://gadm.org/data.html): The script downloads and extracts the data for both North and South Korea across their various administrative levels. 

- [Korean Geographic Information Institute](https://gadm.org/data.html): The script downloads other national files, including rivers, premier points, mountain peaks, railways, roads and the [Korean Demilitarized Zone](https://en.wikipedia.org/wiki/Korean_Demilitarized_Zone). 

## Outputs

The downloaded and processed data is stored in source-specific directories inside `data/raw` and awaiting further work that's still needed, including: 
- Converting files to common formats — `shp` to `geojson`, for example, with the KGII data.
- Compiling English and Korean names as attributes in the KGII data.
  - `서울특별시` vs. `Seoul`, for example
- Consistent storage on S3 for sharing with other users

## Geography reference

Korean geography can be complicated to understand for outsiders. For reference, here are the administrative divisions of South Korea and North Korea in both English and Korean.

### South Korea administrative divisions

#### Overview
- **Country**: South Korea (대한민국)
- **Provinces** (도, Do)
  - Special City (특별시, Teukbyeolsi) - e.g., Seoul (서울특별시)
  - Metropolitan City (광역시, Gwangyeoksi) - e.g., Busan (부산광역시)
  - Province (도, Do) - e.g., Gyeonggi-do (경기도)
- **Cities/Districts** (시, Si; 구, Gu)
  - Si (시) - Cities not divided into districts, e.g., Suwon-si (수원시)
  - Gu (구) - Districts within a city, especially in metropolitan cities, e.g., Gangnam-gu (강남구)
- **Counties** (군, Gun)
  - Smaller towns and rural areas, e.g., Yeongwol-gun (영월군)
- **Townships** (읍, Eup), **Towns** (면, Myeon), and **Neighborhoods** (동, Dong)
  - Eup (읍) - Larger towns in a county
  - Myeon (면) - Smaller towns in a county
  - Dong (동) - Divisions within cities and districts, especially urban areas

### North Korea administrative divisions

#### Overview
- **Country**: North Korea (조선민주주의인민공화국)
- **Provinces** (도, Do)
  - Province (도, Do) - e.g., South Pyongan (평안남도)
- **Special Cities** (직할시, Jikhalsi) - e.g., Pyongyang (평양직할시)
- **Cities** (시, Si)
- **Counties** (군, Gun)
- **Districts** (구역, Guyeok)
- **Towns and Villages** (읍, Eup; 리, Ri)
  - Eup (읍) - Town centers
  - Ri (리) - Villages or small settlements in rural areas

### Table of administrative divisions

| Level | English | Korean | Example |
|-------|---------|--------|---------|
| Country | Country | 나라 | 대한민국/조선민주주의인민공화국 |
| Provinces | Province | 도 | 경기도/평안남도 |
| Special City | Special City | 특별시 | 서울특별시 |
| Metropolitan City | Metropolitan City | 광역시 | 부산광역시 |
| City | City | 시 | 수원시 |
| District (in city) | District | 구 | 강남구 |
| County | County | 군 | 영월군 |
| Township | Township | 읍 | 중구읍 |
| Town | Town | 면 | 사직면 |
| Neighborhood | Neighborhood | 동 | 명동 |
| Special City (North) | Directly Governed City | 직할시 | 평양직할시 |
| District (North) | District | 구역 | 평천구역 |
| Village | Village | 리 | 송천리 |