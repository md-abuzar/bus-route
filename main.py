from flask import Flask, jsonify, request, json
import pandas as pd
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

@app.route("/api/v1/stops", methods=['GET', 'POST'])
def busroutes():
    try:
        if request.method == 'POST':
            # Assuming route_short_name is passed as JSON data in the request body
            route_short_name = request.json.get('route_short_name')
            filtered_routes = routes_df[routes_df['bus_num'] == route_short_name]
            route_id = filtered_routes['route_id']

            filtered_stop_ids = stop_times_df[stop_times_df['trip_id'] == route_id.to_list()[0]]
            stop_ids = filtered_stop_ids['stop_id']

            stop_list = []
            for stop_id in stop_ids:
                stops = stops_df[stops_df['stop_id'] == stop_id]['stop_name'].tolist()
                stop_list.extend(stops)
            
            return jsonify({'stops': stop_list})
        else:
            return {"error" : "method not allowed"}
    except Exception as e:
        return {"error" : str(e)}




if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
