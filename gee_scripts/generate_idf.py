import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# === 设置文件路径 ===
csv_path = r"D:\git\sihanoukville-hydrology-analysis\gee_scripts\rainfall_point_imerg_2000_2025.csv"

# === 1. 读取和预处理数据 ===
df = pd.read_csv(csv_path)
df["datetime"] = pd.to_datetime(df["datetime"])
df.set_index("datetime", inplace=True)
df = df.resample("30min").mean(numeric_only=True)

# === 2. 定义降雨历时（分钟）===
durations_minutes = [5, 10, 15, 30, 60, 120, 180, 240, 480, 720, 1440]

# === 3. 提取每年每个历时的最大降雨 ===
annual_max_dict = {}
grouped_by_year = df.groupby(df.index.year)

for duration in durations_minutes:
    max_per_year = []
    window_size = duration // 30
    for year, group in grouped_by_year:
        if len(group) >= window_size:
            rolling_sum = group["gpm_precipitation"].rolling(window=window_size).sum()
            max_rainfall = rolling_sum.max()
            max_per_year.append((year, max_rainfall))
    annual_max_dict[duration] = pd.Series(
        [x[1] for x in max_per_year], index=[x[0] for x in max_per_year]
    )

annual_max_df = pd.DataFrame(annual_max_dict)

# === 4. 拟合 Gumbel 分布，计算不同重现期降雨量 ===
return_periods = [2.33, 5, 10, 25, 50, 100]
probabilities = [1 - 1/rp for rp in return_periods]
idf_rainfall_table = pd.DataFrame(index=durations_minutes, columns=return_periods)

for duration in durations_minutes:
    data = annual_max_df[duration].dropna()

    # === 三重清洗防炸 ===
    data = data[data > 0]  # 去除非降雨或错误值
    q_low, q_high = data.quantile(0.01), data.quantile(0.99)
    data = data[(data >= q_low) & (data <= q_high)]
    data = data.astype(np.float64)

    if len(data) > 0:
        try:
            loc, scale = stats.gumbel_r.fit(data)
            for rp, prob in zip(return_periods, probabilities):
                rainfall = stats.gumbel_r.ppf(prob, loc=loc, scale=scale)
                idf_rainfall_table.loc[duration, rp] = rainfall
        except Exception as e:
            print(f"Gumbel拟合失败: duration={duration}min，原因：{e}")

idf_rainfall_table = idf_rainfall_table.astype(float)

# === 5. 计算降雨强度（mm/h）===
idf_intensity_table = idf_rainfall_table.div([d/60 for d in durations_minutes], axis=0)

# === 6. 绘制 IDF 曲线 ===
plt.figure(figsize=(10, 6))
for rp in return_periods:
    plt.plot(idf_intensity_table.index, idf_intensity_table[rp], marker='o', label=f'{rp} yrs')
plt.xscale('log')
plt.xlabel('Duration (minutes)')
plt.ylabel('Rainfall Intensity (mm/h)')
plt.title('IDF Curve - Sihanoukville')
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()

# === 7. 保存为 Excel 文件 ===
idf_rainfall_table.to_excel("idf_rainfall_table.xlsx")
idf_intensity_table.to_excel("idf_intensity_table.xlsx")
