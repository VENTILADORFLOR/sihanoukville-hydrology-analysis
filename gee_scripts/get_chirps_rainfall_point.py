"""
Script: get_chirps_rainfall_point.py
Author: Ying Li
Description:
    Download daily rainfall data (1981–2025) from CHIRPS at a specific point
    using Google Earth Engine Python API. Exports the results to Google Drive as CSV.
"""

import ee
import time

# Initialize the Earth Engine API
ee.Initialize()

# Define the target location (Sihanoukville, Cambodia)
point = ee.Geometry.Point([103.656389, 10.540139])  # Longitude, Latitude

# Load CHIRPS Daily Precipitation Data (1981–2025)
chirps = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY") \
    .filterDate('1981-01-01', '2025-01-01') \
    .select('precipitation')

# Convert each image to a feature with date and precipitation value at the point
def image_to_feature(image):
    value = image.reduceRegion(
        reducer=ee.Reducer.first(),
        geometry=point,
        scale=5000,
        maxPixels=1e9
    ).get('precipitation')

    return ee.Feature(None, {
        'date': image.date().format('YYYY-MM-dd'),
        'precipitation': value
    })

# Map the conversion over the image collection
features = chirps.map(image_to_feature)

# Configure export task to Google Drive
task = ee.batch.Export.table.toDrive(
    collection=ee.FeatureCollection(features),
    description="Rainfall_Point_CHIRPS_1981_2025",
    folder="GEE_Exports",
    fileNamePrefix="rainfall_point_1981_2025",
    fileFormat="CSV"
)

# Start export task
task.start()
print("✅ Export task submitted. Please wait...")

# Monitor the task status
while True:
    status = task.status()
    state = status["state"]

    if state == "COMPLETED":
        print("🎉 Export completed successfully! Check your Google Drive folder 'GEE_Exports'.")
        break
    elif state == "FAILED":
        print(f"❌ Export failed: {status['error_message']}")
        break
    else:
        print(f"⏳ Task state: {state}... waiting...")
        time.sleep(30)
