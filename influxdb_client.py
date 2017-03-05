from influxdb import InfluxDBClient

def client():
    return InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'analytics')
