

#Based on zones: http://localhost:8000?zone=5&time_start=2005-01-31T00:00:00Z&time_end=2006-04-18T07:00:00Z
#Based on cities: http://localhost:8000?city=Atlanta&time_start=2005-01-31T00:00:00Z&time_end=2006-04-18T07:00:00Z
#Based on hour of the day: http://localhost:8000?zone=3&hour=15&time_start=2005-01-31T00:00:00Z&time_end=2006-04-18T07:00:00Z
#Based on category: http://localhost:8000?category=Blue&time_start=2005-01-31T00:00:00Z&time_end=2006-04-18T07:00:00Z
#Based on stats: http://localhost:8000?zone=7&stat=avg_per_day&time_start=2005-01-31T00:00:00Z&time_end=2006-04-18T07:00:00Z

def construct_query (query):
    '''
        compile whole query:
    '''
    select = construct_select_statement(query)
    where = construct_where_statement(query)
    full_query = '{0} from power_load {1}'.format(select, where)
    return full_query

def construct_select_statement (query):
    '''
        construct select statement:
    '''
    select = "select "

    aggregation_options = ['max', 'min', 'average']

    # appends aggregation if presented
    if query.get("aggregation") and (query.get("aggregation") in aggregation_options) :
        select += query["aggregation"]

    select += '(value) '

    return select

def construct_where_row (filter):
    '''
        construct filter row where statement
    '''
    rowFilters = []
    row = ''
    filter_options = ['zone_id', 'category', 'city', 'time_start', 'time_end']

    #checks if filter key is acceptable, and if so, append to where statement
    for key in filter.keys():
        if key in filter_options:
            if key == 'time_start':

                rowFilters.append('time >= \'{0}\''.format(str(filter.get(key))))
            elif key == 'time_end':
                rowFilters.append('time <= \'{0}\''.format(str(filter.get(key))))
            else:
                rowFilters.append('{0} = \'{1}\''.format(key, str(filter.get(key))))

    if len(rowFilters) > 0:
        row = '( {0} )'.format(' and '.join(rowFilters))

    return row

def construct_where_statement (query):
    '''
    construct aggregate filter where statement
    '''
    where = ''

    # constructs each filter row
    if query.get("filters") and len(query.get("filters")) > 0:
        filter_array = []
        for filter in query.get("filters"):
            filter_array.append(construct_where_row(filter))
        filters = ' or '.join(filter_array)
        where += 'where ' + filters

    return where
