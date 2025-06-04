import ee
import time

# 初始化 Google Earth Engine
ee.Initialize(project='my project id')

# 定义柬埔寨西哈努克省的研究区域（更新后的经纬度范围）
region = ee.Geometry.BBox(103.416998, 10.392559, 103.950503, 10.874039)

# 选择 Copernicus DEM 30m 数据集，并合成单张影像
copernicus = ee.ImageCollection("COPERNICUS/DEM/GLO30").mosaic().clip(region)

# **确保高程数据是 Float32 类型**
copernicus = copernicus.toFloat()

# 配置导出任务
task = ee.batch.Export.image.toDrive(
    image=copernicus,
    description="Sihanoukville_Copernicus30m_Small",
    folder="GEE_Exports",
    fileNamePrefix="sihanoukville_copernicus30m_small1",
    region=region,
    scale=30,  # Copernicus DEM 分辨率 30m
    maxPixels=1e13,
    fileFormat="GeoTIFF"
)

# 启动任务
task.start()
print("✅ Copernicus 30m 高程数据下载任务已提交！请稍候...")

# **检查任务状态**
while True:
    status = task.status()
    state = status["state"]
    
    if state == "COMPLETED":
        print("🎉 下载完成！请在 Google Drive 'GEE_Exports' 文件夹查看。")
        break
    elif state == "FAILED":
        print(f"❌ 任务失败！错误信息: {status['error_message']}")
        break
    else:
        print(f"⏳ 任务状态: {state}，请稍等...")
        time.sleep(30)  # 每 30 秒检查一次状态
