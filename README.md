# 🌧️ 西哈努克省水文分析 | Hydrological Analysis in Sihanoukville, Cambodia

本项目致力于对柬埔寨西哈努克省的地形与降雨数据进行系统的水文分析，核心目标是通过 Google Earth Engine 和 Python 构建局地的 IDF（强度-历时-频率）曲线，为雨洪管理与城市基础设施规划提供科学依据。

This project focuses on hydrological analysis in Sihanoukville Province, Cambodia, using elevation and rainfall data to derive IDF curves with Google Earth Engine (GEE) and Python. It aims to support stormwater management and infrastructure planning.

---

## 🔍 项目目标 | Objectives

- 获取并分析西哈努克省的高程（DEM）数据
- 使用 GEE 提取 CHIRPS / IMERG 等降雨数据
- 建立降雨时序分析与数据清洗逻辑
- 拟合 IDF 曲线，生成IDF表格，为不同设计重现期提供参考
- 构建跨平台数据处理与可视化工具

---
## 🧰 使用工具 | Tools & Libraries

- Google Earth Engine (Python API + JS Editor)
- Python 3.9+
  - pandas / numpy / matplotlib / scipy
- Jupyter Notebook
- 地理数据集：
  - ALOS 12.5M（高程）
  - CHIRPS Daily / GPM IMERG（降雨）

---

## 📁 项目结构 | Project Structure

```bash
sihanoukville-hydrology-analysis/
├── gee_scripts/             # GEE 脚本（JS 或 Python API）用于提取高程与降雨数据
│   ├── extract_dem.js
│   └── get_rainfall_timeseries.py
│
├── notebooks/               # Python 分析与 IDF 拟合的 Jupyter Notebook
│   └── idf_analysis.ipynb
│
├── data/                    # 存放原始数据或说明（如 CSV、GeoTIFF）
├── outputs/                 # 图表、拟合结果等
├── README.md                # 本文件
├── requirements.txt         # Python 依赖列表
└── .gitignore               # 忽略不需要上传的文件
