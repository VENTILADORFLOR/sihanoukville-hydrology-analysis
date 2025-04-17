import ee
import time

# 初始化 Earth Engine
ee.Initialize(project='proven-dryad-452106')

# 设置坐标点（西哈努克市）
point = ee.Geometry.Point([103.656389, 10.540139])

# 加载 CHIRPS 降雨数据（1981 到 2025）
chirps = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY") \
    .filterDate('1981-01-01', '2025-01-01') \
    .select('precipitation')

# 将图像转换为 Feature（提取点值和日期）
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

# 映射为 FeatureCollection
features = chirps.map(image_to_feature)

# 配置导出任务（导出到 Google Drive）
task = ee.batch.Export.table.toDrive(
    collection=ee.FeatureCollection(features),
    description="Rainfall_Point_CHIRPS_1981_2025",
    folder="GEE_Exports",
    fileNamePrefix="rainfall_point_1981_2025_1",
    fileFormat="CSV"
)

# 启动任务
task.start()
print("✅ 降雨数据导出任务已提交，请稍候...")

# 自动检查任务状态
while True:
    status = task.status()
    state = status["state"]

    if state == "COMPLETED":
        print("🎉 降雨数据导出成功！请在 Google Drive 的 'GEE_Exports' 文件夹中查看。")
        break
    elif state == "FAILED":
        print(f"❌ 任务失败！错误信息: {status['error_message']}")
        break
    else:
        print(f"⏳ 当前任务状态: {state}，继续等待...")
        time.sleep(30) 
