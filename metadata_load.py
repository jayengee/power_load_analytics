import petl as etl
import openpyxl

# import metadata
def get_metadata ():
    metadata = etl.fromcsv('data_sources/zone_data.csv')
    metadata = etl.rename(metadata, {'Zone': 'zone_id', 'City': 'city', 'Category': 'category'})
    metadata = etl.convert(metadata, { 'zone_id': int })
    return etl.dicts(metadata)
