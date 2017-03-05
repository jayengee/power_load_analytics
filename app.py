#!flask/bin/python
from flask import Flask, jsonify
from influxdb_client import client as influxdb
import query_constructor

@app.route('/api/v0.1/query', methods=['POST'])
def querier():
    if not request.json:
        abort(400)
    query = query_constructor.construct(request.json)
    return influxdb().query(query)

if __name__ == '__main__':
    app.run(debug=True)
