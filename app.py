#!flask/bin/python
from flask import Flask, jsonify, request
from influxdb_client import client as influxdb
import query_constructor

app = Flask(__name__)

@app.route('/api/v0.1/status', methods=['GET', 'POST'])
def status():
    '''
        returns 'ok' if server is responsive
    '''
    return jsonify({'ok': True})


@app.route('/api/v0.1/raw_query', methods=['POST'])
def raw_querier():
    '''
        returns results of raw influxql query
    '''
    if not request.json:
        abort(400)
    try:
        rs = influxdb().query(request.json['query'])
        rs = list(rs.get_points())
        return jsonify({ 'ok': True, 'results': rs })
    except:
        print('Unexpected error')

@app.route('/api/v0.1/query', methods=['POST'])
def querier():
    '''
        returns results of constructed query
    '''
    if not request.json:
        abort(400)
    try:
        query = query_constructor.construct_query(request.json['query'])
        rs = influxdb().query(query)
        rs = list(rs.get_points())
        return jsonify({ 'ok': True, 'results': rs })
    except:
        print('Unexpected error')

if __name__ == '__main__':
    app.run(debug=True)
