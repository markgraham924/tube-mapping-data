from flask import Flask, Blueprint, jsonify, make_response, request
from dataset import station, stations, lines, getRoute
from flask_cors import CORS


api_blueprint = Blueprint('api', __name__, url_prefix='/api')
app = Flask(__name__)
CORS(app)


#function to return a single station and it's data
@api_blueprint.route('/station/<string:station_name>', methods=['GET'])
def get_station(station_name):
    stationname, response, status = station(station_name)
    return make_response(jsonify(stationname, response), status)

#returns a list of all station names
@api_blueprint.route('/stations', methods=['GET'])
def get_station_names():
    limit = request.args.get('limit', default=None, type=int)
    zone = request.args.get('zone', default=None, type=str)
    if zone:
        zones = zone.split(',')
    else:
        zones = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    response, status = stations(limit, zones)
    return make_response(jsonify(response), status)

#returns a list of all lines
@api_blueprint.route('/lines', methods=['GET'])
def get_lines():
    response, status = lines()
    return make_response(jsonify(response), status)

#returns the route from one station to another
@api_blueprint.route('/findRoute/<string:start_station>/<string:end_station>', methods=['GET'])
def findRoute(start_station, end_station):
    #check if the stations exist
    start_station, start_station_data, statusS = station(start_station)
    end_station, end_station_data, statusE = station(end_station)
    if statusS != 200:
        return make_response(jsonify({'Error': 'Start Station (' + start_station + ') Not Found'}), statusS)
    if statusE != 200:
        return make_response(jsonify({'Error': 'End Station (' + end_station + ') Not Found'}), statusE)
    path,total_time = getRoute(start_station, end_station)#path, cost = 
    return make_response(jsonify({'path': path, 'cost': total_time}), 200)
    #return make_response(jsonify({'path': path, 'cost': cost}), 200)
    
    


app.register_blueprint(api_blueprint)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Choose whichever port you prefer

