import subprocess
import pandas as pd

def make_http2_call(url : str) -> str:
    # The Docker command
    docker_command = (
        'curl --http2 -o /dev/null '
        '-w "DNS lookup: %{time_namelookup} seconds\n'
        'Connect: %{time_connect} seconds\n'
        'TLS handshake: %{time_appconnect} seconds\n'
        'Start transfer: %{time_starttransfer} seconds\n'
        'Total time: %{time_total} seconds\n" '
        f'{url}'
    )

    # Run the command
    try:
        result = subprocess.run(docker_command, shell=True, text=True, capture_output=True, check=True)
        return result.stdout  # Print the output of the command
    except Exception as e:
        print(f"Command failed with error: {e.stderr} and error {e}")


def make_http3_call(url : str) -> str:
    # The Docker command
    docker_command = (
        'docker run -it --rm ymuski/curl-http3 curl --http3 -o /dev/null '
        '-w "DNS lookup: %{time_namelookup} seconds\n'
        'Connect: %{time_connect} seconds\n'
        'TLS handshake: %{time_appconnect} seconds\n'
        'Start transfer: %{time_starttransfer} seconds\n'
        'Total time: %{time_total} seconds\n" '
        f'{url}'
    )

    # Run the command
    try:
        result = subprocess.run(docker_command, shell=True, text=True, capture_output=True, check=True)
        return result.stdout  # Print the output of the command
    except Exception as e:
        print(f"Command failed with error: {e.stderr} and error {e}")


def get_toal_time_from_curl_output(curl_output : str) -> float: return float(curl_output.split('seconds\n')[-2].split(':')[1])


latencies = {
    'http2' : [],
    'http3' : [],
}

for i in range(100):
    url = 'https://blog.cloudflare.com'
    curl_output_http3 = make_http3_call(url)
    curl_output_http2 = make_http2_call(url)
    total_time_http3 = get_toal_time_from_curl_output(curl_output_http3)
    total_time_http2 = get_toal_time_from_curl_output(curl_output_http2)
    latencies['http3'].append(total_time_http3)
    latencies['http2'].append(total_time_http2)

latencies_series = pd.DataFrame(latencies)

print(
    f"""
    HTTP/2 LATENCY : {latencies_series['http2'].mean()}
    HTTP/3 LATENCY : {latencies_series['http3'].mean()}
    """
)