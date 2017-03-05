from influxdb import InfluxDBClient
import datetime
import petl as etl
import time

# One-time date import script

# import points data from .csv, and reformat
data_rows = etl.fromcsv('data_sources/Load_history_ver2.csv')
data_rows = etl.convert(data_rows, {
    'zone_id': int,
    'year': int,
    'month': int,
    'day': int,
    'h1': float,
    'h2': float,
    'h3': float,
    'h4': float,
    'h5': float,
    'h6': float,
    'h7': float,
    'h8': float,
    'h9': float,
    'h10': float,
    'h11': float,
    'h12': float,
    'h13': float,
    'h14': float,
    'h15': float,
    'h16': float,
    'h17': float,
    'h18': float,
    'h19': float,
    'h20': float,
    'h21': float,
    'h22': float,
    'h23': float,
    'h24': float
})
data_rows = etl.dicts(data_rows)

# transform points into format for ingestion into influxdb

#define hours
hours = map(lambda x: 'h'+str(x), range(1, 25))

#transform array of data into points for nflxudb insertion
def transform_rows_into_points (rows):
    points = []
    for row in rows:
        for hour in hours:
            if not row.get(hour) or row[hour] == '':
                continue
            else:
                time = datetime.datetime(row['year'], row['month'], row['day'], int(hour.replace('h', '')) - 1)

            new_dict = {
                'measurement': 'power_load',
                'tags': {
                    'zone_id': row['zone_id'],
                },
                'time': time,
                'fields': {
                    'value': row[hour],
                }
            }
            points.append(new_dict)
    return points

points = transform_rows_into_points(data_rows)

print '--n records: '
print len(points)
print '--first record: '
print points[0]


# establishes inluxdb connection
client = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'analytics')
client.create_database('analytics')

# chunks out payloads for size x
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

chunked_points = chunks(points, 5000)
chunk_counter = 1

# send to influxdb
for chunk in chunked_points:
    print '--sending chunk {} '.format(chunk_counter)
    client.write_points(chunk)
    chunk_counter += 1
    time.sleep(2)
