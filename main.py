from flask import Flask, jsonify, request, json
import pandas as pd
from flask_cors import CORS
from google.transit import gtfs_realtime_pb2
import requests
from geopy.geocoders import Nominatim

routes_df = pd.read_csv("routes.csv")
trips_df = pd.read_csv("trips.csv")
stop_times_df = pd.read_csv("stop_times.csv")
stops_df = pd.read_csv("stops.csv")

routes_pmpl_df = pd.read_csv("pmpl/routes.csv")
trips_pmpl_df = pd.read_csv("pmpl/trips.csv")
stop_times_pmpl_df = pd.read_csv("pmpl/stop_times.csv")
stops_pmpl_df = pd.read_csv("pmpl/stops.csv")


app = Flask(__name__)
CORS(app)
geolocator = Nominatim(user_agent="bus_route_App")


@app.route("/api/v1/routes")
def busnum():
    routes = routes_df['bus_num'].tolist()
    return jsonify(routes)

@app.route("/api/v1/routes_long_name")
def routeLongName():
    route_long_name = routes_df['route_long_name'].tolist()
    return jsonify(route_long_name)

@app.route("/api/v1/num", methods=['GET', 'POST'])
def busshortnum():
    try:
        route = request.json.get('route')
        filtered_num = routes_df[routes_df['bus_num'] == route]
        num = filtered_num['route_long_name'].tolist()
        return jsonify(num)
    except Exception as e:
        return {"error" : str(e)}

@app.route("/api/v1/stops", methods=['GET', 'POST'])
def busroutes():
    try:
        if request.method == 'POST':
            # Assuming route_short_name is passed as JSON data in the request body
            route_short_name = request.json.get('route_short_name')
            filtered_routes = routes_df[routes_df['route_long_name'] == route_short_name]
            route_id = filtered_routes['route_id']

            filtered_stop_ids = stop_times_df[stop_times_df['trip_id'] == route_id.to_list()[0]]
            stop_ids = filtered_stop_ids['stop_id']

            stop_list = []
            for stop_id in stop_ids:
                stop_data = stops_df[stops_df['stop_id'] == stop_id][['stop_name', 'stop_lat', 'stop_lon']].to_dict(orient='records')
                stop_list.extend(stop_data)
            
            return jsonify({'stops': stop_list})
        else:
            return {"error" : "method not allowed"}
    except Exception as e:
        return {"error" : str(e)}
    


@app.route("/api/v1/track/live", methods=['GET', 'POST'])
def buslive():
    try:
        if request.method == 'POST':
            route_short_name = request.json.get('route_short_name')
            filtered_routes = routes_df[routes_df['route_long_name'] == route_short_name]
            route_id = filtered_routes['route_id'].tolist()[0]
            feed = gtfs_realtime_pb2.FeedMessage()
            response = requests.get('https://otd.delhi.gov.in/api/realtime/VehiclePositions.pb?key=NBffniFfJNj2vHB67r3t0fdkVtkc76a0')
            feed.ParseFromString(response.content)
            lat_lon = []
            for entity in feed.entity:
                if entity.vehicle.trip.route_id == str(route_id):
                    lat_lon.append((entity.vehicle.position.latitude, entity.vehicle.position.longitude))
                
            return jsonify({'live_lat_lon': lat_lon})
        else:
            return {"error" : "method not allowed"}
    except Exception as e:
        return {"error" : str(e)}
    
    

    
            
    ''' location = geolocator.reverse((entity.vehicle.position.latitude, entity.vehicle.position.longitude), exactly_one=True)
            print (location.address if location else "Unknown location")
            return jsonify({
                'latitude':entity.vehicle.position.latitude,
                'longitude':entity.vehicle.position.longitude,        
                })
        
            lat_lon.append(entity.vehicle.position.latitude, entity.vehicle.position.longitude)

            print(lat_lon)'''

@app.route("/api/v1/pmpl/routes")
def pmpmlbusnum():
    routes = trips_pmpl_df['route_short_name'].tolist()
    return jsonify(routes)

@app.route("/api/v1/pmpml/num", methods=['GET', 'POST'])
def pmpmlbusshortnum():
    try:
        route = request.json.get('route')
        filtered_num = trips_pmpl_df[trips_pmpl_df['route_short_name'] == route]
        num = filtered_num['route_id'].tolist()[0]
        return jsonify(num)
    except Exception as e:
        return {"error" : str(e)}


@app.route("/api/v1/pmpl/stops", methods=['GET', 'POST'])
def pmpmlbusroutes():
    try:
        if request.method == 'POST':
            route_id = request.json.get('route_id')
            filtered_trips_df = trips_pmpl_df[trips_pmpl_df['route_id'] == route_id]
            trip_id = filtered_trips_df['trip_id'].tolist()[0]

            filtered_stop_times_df = stop_times_pmpl_df[stop_times_pmpl_df['trip_id'] == trip_id]
            print(filtered_stop_times_df)
            stop_ids = filtered_stop_times_df['stop_id'].tolist()
            
            stop_list = []
            for stop_id in stop_ids:
                stop_data = stops_pmpl_df[stops_pmpl_df['stop_id'] == stop_id][['stop_name', 'stop_lat', 'stop_lon']].to_dict(orient='records')
                stop_list.extend(stop_data)
            
            return jsonify({'stops': stop_list})

        else:
            return {"error" : "method not allowed"}
    except Exception as e:
        return {"error" : str(e)}

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
