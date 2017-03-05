import petl as etl
import openpyxl

# import metadata
def get_metadata:
    metadata = etl.fromxlsx('data_sources/sampling_coordinates.xlsx', read_only=True)
    metadata = etl.dicts(metadata)
