import ee
import time

# 初始化 Earth Engine
ee.Initialize(project='proven')

# Define the target location (Sihanoukville, Cambodia)
point = ee.Geometry.Point([103.656389, 10.540139])  # Longitude, Latitude

# Load GPM IMERG Final Precipitation Data
imerg = ee.ImageCollection("NASA/GPM_L3/IMERG_V07") \
    .filterDate('2000-06-01', '2025-01-01') \
    .select('precipitation')

# Convert image to feature
def image_to_feature(image):
    value = image.reduceRegion(
        reducer=ee.Reducer.first(),
        geometry=point,
        scale=5000,
        maxPixels=1e9
    ).get('precipitation')

    return ee.Feature(None, {
        'datetime': image.date().format('YYYY-MM-dd HH:mm'),
        'gpm_precipitation': value
    })

# Map the conversion over the image collection
features = imerg.map(image_to_feature)

# Configure export task to Google Drive
task = ee.batch.Export.table.toDrive(
    collection=ee.FeatureCollection(features),
    description="Rainfall_Point_IMERG_2000_2025",
    folder="GEE_Exports",
    fileNamePrefix="rainfall_point_imerg_2000_2025",
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
