from influxdb_client import client as influxdb
from points_extract_transform import get_data as points
import time

def sent_to_influx ():
    '''
        grabs points and metadata and sends to influxd
    '''

    # establishes db, if not already present
    influxdb().create_database('analytics')

    # chunks out payloads for size x
    def chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i+n]

    chunked_points = chunks(points(), 5000)
    chunk_counter = 1

    # send to influxdb
    for chunk in chunked_points:
        print '--sending chunk {} '.format(chunk_counter)
        influxdb().write_points(chunk)
        chunk_counter += 1
        time.sleep(2)
