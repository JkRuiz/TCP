import requests
import psutil
import json
import datetime
from urllib.request import urlopen

url = "http://157.253.205.122:5000/{}"
createMetric = "metrics"


def send_metric():
    metric = get_metrics()
    jsonPost = build_json(metric)
    post_metric(jsonPost)


def get_metrics():
    network_stats = psutil.net_io_counters()
    # network_stats on format: snetio(bytes_sent=5665173504, bytes_recv=18591582208, packets_sent=11822078, packets_recv=19544923, errin=0, errout=0, dropin=0, dropout=0)
    bytesReceived = network_stats[1]
    return str(bytesReceived)


def build_json(bytesR):
    ip = str(urlopen('http://ip.42.pl/raw').read().decode("utf-8"))
    time = str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    data = {"ipClient": ip, "bytes": bytesR, "time": time}
    json_data = json.dumps(data)
    return json_data


def post_metric(payload):
    return requests.post(url.format(createMetric), json=payload)
