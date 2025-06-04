# 🌧️ Hydrological Analysis in Sihanoukville, Cambodia

This project focuses on hydrological analysis in Sihanoukville Province, Cambodia, using elevation and rainfall data to derive IDF curves with Google Earth Engine (GEE) and Python. It aims to support stormwater management and infrastructure planning.

---

## 🔍 Objectives

- Acquire and analyze Digital Elevation Model (DEM) data for Sihanoukville
- Extract rainfall data from CHIRPS / IMERG via GEE
- Establish rainfall time-series processing and data cleaning workflows
- Fit IDF curves and generate tables for multiple design return periods
- Build cross-platform tools for data processing and visualization

---
## 🧰 Tools & Libraries

- Google Earth Engine (Python API + JS Editor)
- Python 3.9+
  - pandas / numpy / matplotlib / scipy
- Jupyter Notebook
- Geospatial datasets:
  - ALOS 12.5M (elevation)
  - CHIRPS Daily / GPM IMERG (precipitation)

---

## 📁 Project Structure

```bash
sihanoukville-hydrology-analysis/
├── gee_scripts/                         # Core GEE scripts and analysis components
│   ├── chirps.py                        # Download CHIRPS daily rainfall data (1981–present)
│   ├── get_alos_dem.py                  # Download ALOS 12.5m DEM elevation data
│   ├── sihanoukville_alos12m_ream.tif   # ALOS 12.5m DEM elevation data
│   ├── get_imerg_rainfall_point.py      # Extract GPM IMERG rainfall data for a target point (2000–2025)
│   ├── generate_idf.py                  # Fit IDF curves from IMERG time-series and generate tables
│   ├── rainfall_point_imerg_2000_2025.csv       # Raw point rainfall data (IMERG 2000–2025)
│   ├── idf_rainfall_table.xlsx          # Fitted rainfall depth IDF table (unit: mm)
│   ├── idf_intensity_table.xlsx         # Fitted rainfall intensity IDF table (unit: mm/h)
│   ├── Sihanoukville_IDF_Table.docx     # Summary of rainfall depth and intensity tables (Word format)
│   ├── IDF Curve_Sihanoukville.png      # IDF curve plot (visualization result)
│   ├── IDF TABLE.jpg                    # Historical IDF table from local government station (scanned image)
│   ├── COPERNICUS.py                    # Download COPERNICUS 30 m DEM elevation data
│   ├── aster.py                         # Download aster 30 m DEM elevation data
│   └── SRTM30m.py                       # Download SRTM 30 m DEM elevation data
│
├── README.md                            # Project documentation (this file)
├── requirements.txt                     # Python dependency list
└── .gitignore                           # Git ignore file configuration

