"""
Script: get_alos_dem.py
Author: Ying Li
Description:
    Export ALOS PALSAR 12.5m DSM data for Sihanoukville region using
    Google Earth Engine Python API. Data will be exported to Google Drive.
"""

import ee
import time

# Initialize Google Earth Engine
ee.Initialize()

# Load ALOS PALSAR 12.5m DSM (AW3D30 v3.2) and mosaic into one image
dataset = ee.ImageCollection("JAXA/ALOS/AW3D30/V3_2").mosaic()

# Define target region (Sihanoukville, Cambodia) as a bounding box
region = ee.Geometry.Rectangle([103.416998, 10.392559, 103.950503, 10.874039])

# Select Digital Surface Model (DSM) and clip to region
elevation = dataset.select("DSM").clip(region)

# Configure export task to Google Drive
task = ee.batch.Export.image.toDrive(
    image=elevation,
    description="Sihanoukville_ALOS_12m_Elevation_Small",
    folder="GEE_Exports",
    fileNamePrefix="sihanoukville_alos12m_small",
    region=region,
    scale=12.5,
    maxPixels=1e13,
    fileFormat="GeoTIFF"
)

# Start the export task
task.start()
print("✅ ALOS 12.5m elevation export task submitted. Please wait...")

# Check task status every 30 seconds
while True:
    status = task.status()
    state = status["state"]

    if state == "COMPLETED":
        print("🎉 Export completed! Check 'GEE_Exports' folder in Google Drive.")
        break
    elif state == "FAILED":
        print(f"❌ Export failed: {status['error_message']}")
        break
    else:
        print(f"⏳ Task status: {state}... waiting...")
        time.sleep(30)
