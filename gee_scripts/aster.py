import ee
import time

# 初始化 Google Earth Engine
ee.Initialize(project='proven-dryad-452106-j9')

# 选择 ASTER GDEM 数据集
dataset = ee.Image("NASA/ASTER_GED/AG100_003")  # 最新 ASTER GDEM 数据集

# 定义研究区域（柬埔寨西哈努克省）
region = ee.Geometry.Rectangle([103.416998, 10.392559, 103.950503, 10.874039])

# 选择高程波段 "elevation" 并裁剪到研究区域
elevation = dataset.select("elevation").clip(region)

# 配置导出任务
task = ee.batch.Export.image.toDrive(
    image=elevation,
    description="Sihanoukville_ASTER_Elevation",
    folder="GEE_Exports",
    fileNamePrefix="sihanoukville_aster",
    region=region,
    scale=30,  # 30米分辨率
    maxPixels=1e13,
    fileFormat="GeoTIFF"
)

# 启动任务
task.start()
print("✅ ASTER GDEM 30m 高程数据下载任务已提交！请稍候...")

# 检查任务状态
while True:
    status = task.status()
    state = status["state"]
    
    if state == "COMPLETED":
        print("🎉 下载完成！请在 Google Drive 查看 'GEE_Exports' 文件夹。")
        break
    elif state == "FAILED":
        print(f"❌ 任务失败！错误信息: {status['error_message']}")
        break
    else:
        print(f"⏳ 任务状态: {state}，请稍等...")
        time.sleep(30)  # 每 30 秒检查一次状态
