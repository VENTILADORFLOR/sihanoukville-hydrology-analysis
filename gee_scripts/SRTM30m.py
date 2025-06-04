import ee
import time

# 初始化 Google Earth Engine
ee.Initialize(project='proven-dryad-452106-j9')

# 定义柬埔寨西哈努克省（西港）的研究区域（匹配您的经纬度范围）
region = ee.Geometry.BBox(103.416998, 10.392559, 103.950503, 10.874039)

# 选择 SRTM 数据集
srtm = ee.Image("USGS/SRTMGL1_003").clip(region)  # SRTM 30m 数据

# **确保数据是 Float32 类型**
srtm = srtm.toFloat()

# 配置导出任务
task = ee.batch.Export.image.toDrive(
    image=srtm,
    description="Sihanoukville_SRTM30m",
    folder="GEE_Exports",
    fileNamePrefix="sihanoukville_srtm30m",
    region=region,
    scale=30,  # SRTM 分辨率 30m
    maxPixels=1e13,
    fileFormat="GeoTIFF"
)

# 启动任务
task.start()
print("✅ SRTM 30m 高程数据下载任务已提交！请稍候...")

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
