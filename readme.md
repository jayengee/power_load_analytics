# power_load_analytics

## Overview ##
Data ingestion scripts and API for power load metrics written in Flask, ETL-ing from .csv's and storing into/querying against a local InfluxDB instance

## Request/Response Endpoints ##

endpoint | params | description
------------- | ------------- | -------------
rawQuery | `rawQuery [object]` | Returns results of raw InfluxQL query passed.
query | `query [Object]` | Returns results of query constructed via query parameters passed

### rawQuery ###
#### Structure ####
```
{
  "query": <string>
}
```
#### Examples ####
get server statistics
{
  "rawQuery": "SHOW STATS"
}


### query ###
#### Structure ####
```
{
  "query": {
      "aggregation": "mean" || "median" || "max" || "min"
      "filters": [
        {
          "city": <string> || "zone_id": <int> || "category": <string> || "time_start": <string> || "time_end": <string>
          ...
        },
        ...
      ]
  }
}
```
#### Examples ####
Get all load measurements from zone 1 from 2003-02-06T05:00:00Z onwards
```
{
  "query": {
  	"filters": [
  		{
  			"zone_id": 1,
  			"time_start": "2003-02-06T05:00:00Z"
  		}
  	]
  }
}
```

Get max load from category blue or red sites
```
{
  "query": {
  	"aggregation": "max",
  	"filters": [
  		{
  			"category": "Blue"
  		},
  		{
  			"category": "Red"
  		}
  	]
  }
}
```
