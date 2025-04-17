import ee
import time

# 初始化 Earth Engine
ee.Initialize(project='proven-dryad-452106-j9')


# 加载 ALOS DSM 数据，并合成单张影像
dataset = ee.ImageCollection("JAXA/ALOS/AW3D30/V3_2").mosaic()

# 定义研究区域（西哈努克省边界）
region = ee.Geometry.Rectangle([103.416998, 10.392559, 103.950503, 10.874039])

# 选择 DSM 波段并裁剪
elevation = dataset.select("DSM").clip(region)

# 配置导出任务，输出到 Google Drive
task = ee.batch.Export.image.toDrive(
    image=elevation,
    description="Sihanoukville_ALOS_12m_Elevation_Small",
    folder="GEE_Exports",
    fileNamePrefix="sihanoukville_alos12m_ream",
    region=region,
    scale=12.5,
    maxPixels=1e13,
    fileFormat="GeoTIFF"
)

# 启动导出任务
task.start()
print("✅ ALOS 12.5m elevation export task submitted. Please wait...")

# 循环检测任务状态
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
