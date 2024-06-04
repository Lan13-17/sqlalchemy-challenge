# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
query_date = "2016-08-23"


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    hawaii_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= query_date).all()
    data = {i[0]:i[1] for i in hawaii_data}
    return jsonify(data)

@app.route("/api/v1.0/stations")
def stations():
    station_data = session.query(station.name).all()
    station_data = [i[0] for i in station_data]
    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    active_station = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    tobs_data = session.query(measurement.tobs).\
        filter(measurement.date >= query_date).\
        filter(measurement.station == active_station[0][0]).all()
    tobs_data = [i[0] for i in tobs_data]
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def start(start):
    tobs_data = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()
    tobs_data = list(tobs_data[0])
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    tobs_data = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()
    tobs_data = list(tobs_data[0])
    return jsonify(tobs_data)

if __name__ == "__main__":
    app.run(debug=True)