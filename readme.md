# power_load_analytics

## Overview ##
Data ingestion scripts and API for power load metrics written in Flask, ETL-ing from .csv's and storing into/querying against a local InfluxDB instance

##Request/Response Endpoints##

endpoint | params | description
------------- | ------------- | -------------
rawQuery | `rawQuery [object]` | Returns results of raw InfluxQL query passed.
query | `query [Object]` | Returns results of query constructed via query parameters passed

###rawQuery###
####Structure####
```
{
  "rawQuery": "SHOW STATS"
}
```
####Examples####

###query###
####Structure####
```
{
  "query": {
      "aggregation": "average" || "median" || "max" || "min"
      "filters": [
        {
          "city": [<string>] || "zone_id": [<int>] || "category": [<string>] || "time_start": <string> || "time_end": <string> || "hour": <int>,
          ...
        },
        ...
      ]
  }
}
```
####Examples####
