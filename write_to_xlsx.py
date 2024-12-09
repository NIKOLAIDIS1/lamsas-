import subprocess
import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
from time import time

def make_http2_call(url: str) -> str:
    docker_command = (
        'docker run -it --rm ymuski/curl-http3 curl --http2 -o /dev/null '
        '-w "DNS lookup: %{time_namelookup} seconds\n'
        'Connect: %{time_connect} seconds\n'
        'TLS handshake: %{time_appconnect} seconds\n'
        'Start transfer: %{time_starttransfer} seconds\n'
        'Total time: %{time_total} seconds\n" '
        f'{url}'
    )

    try:
        result = subprocess.run(docker_command, shell=True, text=True, capture_output=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"HTTP/2 command failed: {e.stderr}")
        return None

def make_http3_call(url: str) -> str:
    docker_command = (
        'docker run -it --rm ymuski/curl-http3 curl --http3 -o /dev/null '
        '-w "DNS lookup: %{time_namelookup} seconds\n'
        'Connect: %{time_connect} seconds\n'
        'TLS handshake: %{time_appconnect} seconds\n'
        'Start transfer: %{time_starttransfer} seconds\n'
        'Total time: %{time_total} seconds\n" '
        f'{url}'
    )

    try:
        result = subprocess.run(docker_command, shell=True, text=True, capture_output=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"HTTP/3 command failed: {e.stderr}")
        return None

def get_total_time_from_curl_output(curl_output: str) -> float:
    # Use regex to extract the total time from curl output
    match = re.search(r"Total time: (\d+\.\d+)", curl_output)
    if match:
        return float(match.group(1))
    else:
        raise Exception("Failed to parse curl output.")

def run_benchmark(url: str) -> dict:
    latencies = {'http2': [], 'http3': []}

    for _ in range(100):
        curl_output_http3 = make_http3_call(url)
        curl_output_http2 = make_http2_call(url)
        
        if curl_output_http3 and curl_output_http2:
            total_time_http3 = get_total_time_from_curl_output(curl_output_http3)
            total_time_http2 = get_total_time_from_curl_output(curl_output_http2)

            if total_time_http3 and total_time_http2:
                latencies['http3'].append(total_time_http3)
                latencies['http2'].append(total_time_http2)

    return latencies


def run_parallel_benchmark(url: str) -> dict:
    latencies = {'http2': [], 'http3': []}

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda _: run_benchmark(url), range(100)))

    # Collect the results from all threads
    for result in results:
        latencies['http2'].extend(result['http2'])
        latencies['http3'].extend(result['http3'])

    return latencies


# URL to test
url = 'https://openai.com'

# Run the benchmark
latencies = run_benchmark(url)

# Create a DataFrame to analyze the results
latencies_series = pd.DataFrame(latencies)

# Print out the average latencies
print(
    f"""
    HTTP/2 LATENCY : {latencies_series['http2'].mean()}
    HTTP/3 LATENCY : {latencies_series['http3'].mean()}
    """
)

latencies_series.to_csv(f'http2-vs-http3_{int(time())}')