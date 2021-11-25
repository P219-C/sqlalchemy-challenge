import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

from flask import Flask, app, jsonify

#==================================================================
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(bind = engine)
# Design a query to retrieve the last 12 months of precipitation data and plot the results
last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
# Converting date in string format into datetime object
last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
# Calculate the date 1 year ago from the last data point in the database
last_year = last_date - dt.timedelta(days=365)
session.close()

#==================================================================
app = Flask("Climate App")

dict_routes = {
    "precipitation": f"/api/v1.0/precipitation",
    "stations": f"/api/v1.0/stations",
    "tobs": f"/api/v1.0/tobs"
}


@app.route("/")
def home():
    text = f"""<h1>Available Routes:</h1>
    <p>
        <h2>Precipitation</h2>
        <p>Presents the last 12 months of precipitation data.</p>
        <p>Dictionary name: 'precipitation_dict'   ===>   Key: 'date' | Value: 'prcp' (precipitation)</p>       
        <a target="_blank" href="http://127.0.0.1:5000/{dict_routes['precipitation']}">Click here: {dict_routes['precipitation']}</a>
    </p>
    <p>
        <h2>Stations</h2>
        <p>Returns a JSON list of stations from the dataset:</p>
        <a target="_blank" href="http://127.0.0.1:5000/{dict_routes['stations']}">Click here: {dict_routes['stations']}</a>
    </p>
    <p>
        <h2>Observed temperature</h2>
        <a target="_blank" href="http://127.0.0.1:5000/{dict_routes['tobs']}">Click here: {dict_routes['tobs']}</a>
    </p>"""
    
    return text



@app.route(dict_routes['precipitation'])
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(bind = engine)
    # Perform a query to retrieve the data and precipitation scores
    query1 = session.query(Measurement.station, Measurement.date, Measurement.prcp, Measurement.tobs).filter(Measurement.date >= last_year).order_by(Measurement.date).all()
    session.close()

    precipitation_dict = {}
    for station, date, prcp, tobs in query1:
        precipitation_dict[date] = prcp

    return precipitation_dict
    

@app.route(dict_routes['stations'])
def stations():
    session = Session(bind = engine)
    query1 = session.query(Station.station).all()
    session.close()

    all_stations = []

    for row in query1:
        all_stations.append(row[0])

    return jsonify(all_stations)

@app.route(dict_routes['tobs'])
def tobs():
    session = Session(bind=engine)
    query1 = session.query(Station.station).all()
    

    station_dict = {}
    for station in query1:
        station_dict[station[0]] = session.query(Measurement.date).filter(Measurement.station == station[0]).count()

    most_active_station = max(station_dict, key=station_dict.get)

    query2 = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= last_year).filter(Measurement.station == most_active_station).order_by(Measurement.date).all()
    session.close()

    date_tobs_list = []
    for row in query2:
        date_tobs_list.append([row[0], row[1]])

    return jsonify(date_tobs_list)

# @app.route("/api/v1.0<start>")

if __name__ == "__main__":
    app.run(debug=True)