from flask import Flask, jsonify, request, json
import pandas as pd
from flask_cors import CORS
routes_df = pd.read_csv("routes.csv")
trips_df = pd.read_csv("trips.csv")
stop_times_df = pd.read_csv("stop_times.csv")
stops_df = pd.read_csv("stops.csv")


app = Flask(__name__)
CORS(app)

@app.route("/api/v1/routes")
def busnum():
    routes = routes_df['bus_num'].tolist()
    return jsonify(routes)

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




if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
