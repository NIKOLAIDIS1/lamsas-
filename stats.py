import subprocess
import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

# Create a DataFrame to analyze the results
latencies_series = pd.read_csv('http2-vs-http3_1733409642')

# Print out the average latencies
print(
    f"""
    HTTP/2 LATENCY : {latencies_series['http2'].mean()}
    HTTP/3 LATENCY : {latencies_series['http3'].mean()}
    """
)

# Calculate additional metrics
http2_metrics = {
    'mean': latencies_series['http2'].mean(),
    'median': latencies_series['http2'].median(),
    'std_dev': latencies_series['http2'].std(),
    'min': latencies_series['http2'].min(),
    'max': latencies_series['http2'].max(),
    'percentile_25': latencies_series['http2'].quantile(0.25),
    'percentile_75': latencies_series['http2'].quantile(0.75),
}

http3_metrics = {
    'mean': latencies_series['http3'].mean(),
    'median': latencies_series['http3'].median(),
    'std_dev': latencies_series['http3'].std(),
    'min': latencies_series['http3'].min(),
    'max': latencies_series['http3'].max(),
    'percentile_25': latencies_series['http3'].quantile(0.25),
    'percentile_75': latencies_series['http3'].quantile(0.75),
}

# Print metrics
print("HTTP/2 Metrics:", http2_metrics)
print("HTTP/3 Metrics:", http3_metrics)

# Visualize metrics
plt.figure(figsize=(12, 6))

# Boxplot
plt.subplot(1, 2, 1)
plt.boxplot([latencies_series['http2'], latencies_series['http3']], labels=['HTTP/2', 'HTTP/3'])
plt.title('Boxplot of Latencies')
plt.ylabel('Latency (seconds)')

# Histogram
plt.subplot(1, 2, 2)
plt.hist(latencies_series['http2'], bins=30, alpha=0.7, label='HTTP/2', color='blue')
plt.hist(latencies_series['http3'], bins=30, alpha=0.7, label='HTTP/3', color='green')
plt.title('Histogram of Latencies')
plt.xlabel('Latency (seconds)')
plt.ylabel('Frequency')
plt.legend()

# Show plots
plt.tight_layout()
plt.show()

