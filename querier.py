from dateutil.parser import *
from influxdb import InfluxDBClient
import petl as etl
import time


client = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'analytics')
