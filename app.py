#!flask/bin/python
from flask import Flask, jsonify, request
from influxdb_client import client as influxdb
import query_constructor

app = Flask(__name__)

# returns 'ok' if server is responsive
@app.route('/api/v0.1/status', methods=['GET', 'POST'])
def status():
    return jsonify({'ok': True})

# returns results of raw influxql query
@app.route('/api/v0.1/raw_query', methods=['POST'])
def raw_querier():
    if not request.json:
        abort(400)
    rs = influxdb().query(request.json['query'])
    rs = list(rs.get_points())
    return jsonify({ 'ok': True, 'results': rs })

# returns results of constructed query
@app.route('/api/v0.1/query', methods=['POST'])
def querier():
    if not request.json:
        abort(400)
    query = query_constructor.construct_query(request.json['query'])
    print query
    rs = influxdb().query(query)
    rs = list(rs.get_points())
    return jsonify({ 'ok': True, 'results': rs })

if __name__ == '__main__':
    app.run(debug=True)
