import datetime
from metadata_load import get_metadata
import petl as etl

def get_data ():
    '''
        import points data from .csv, and reformat
    '''
    data_rows = etl.fromcsv('data_sources/Load_history_ver2.csv')
    data_rows_map = {
        'zone_id': int,
        'year': int,
        'month': int,
        'day': int
    }
    data_rows_map.update({'h{0}'.format(i): float for i in range(1, 25)})
    data_rows = etl.convert(data_rows, data_rows_map)

    #join metadata
    metadata = get_metadata()
    data_rows = etl.join(data_rows, metadata, key = 'zone_id')
    data_rows = etl.dicts(data_rows)

    # transform points into format for ingestion into influxdb

    #define hours
    hours = map(lambda x: 'h'+str(x), range(1, 25))

    def transform_rows_into_points (rows):
        '''
            transform array of data into points for nflxudb insertion
        '''
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
                        'category': row['category'],
                        'city': row['city']
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

    return points
