# import numpy as np

# import sqlalchemy
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine, func

from flask import Flask, app, jsonify

app = Flask("Climate App")

dict_routes = {
    "precipitation": f"/api/v1.0/precipitation",
    "stations": f"/api/v1.0/stations",
    "tobs": f"/api/v1.0/tobs"
}


@app.route("/")
def home():
    text = f"""<h1>Example 2</h1>
    <p>{dict_routes['precipitation']}</p>
    <p>{dict_routes['stations']}</p>
    <p>{dict_routes['tobs']}</p>"""
    
    return text



@app.route(dict_routes['precipitation'])
def precipitation():
    return {"name": "Pablo", "suburb": "Karawara"}

@app.route(dict_routes['stations'])
def stations():
    return "pass"

@app.route(dict_routes['tobs'])
def tobs():
    return "pass"

# @app.route("/api/v1.0<start>")

if __name__ == "__main__":
    app.run(debug=True)