import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the measurement and station tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Avalable Routes:<br/>"
        f"/api/v1.0/precipitation - Precipitation values for last year<br/>"

        f"/api/v1.0/stations - List of stations<br/>"

        f"/api/v1.0/tobs - List of temperature observations for previous year<br/>"

        f"/api/v1.0/&ltstart&gt - List of minimum, average and maximum temperatures for a given <start> date in yyyy-mm-dd format to now<br/>"

        f"/api/v1.0/&ltstart&gt/&ltend&gt - List of minimum, average and maximum temperatures for a given <start> date in yyyy-mm-dd format to a given <end> date in yyyy-mm-dd format<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary of all precipitation values for last year"""
    # Query all dates and tobs for last year from the Measurement table
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > '2017-01-01').all()

    # Convert list of tuples into normal list
    precipitation_list = list(np.ravel(results))
    precipitation_dict = dict(zip(precipitation_list[::2], precipitation_list[1::2]))

    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all stations from the Measurement table
    results = session.query(Measurement.station).\
        group_by(Measurement.station).all()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(results))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature observations for previous year."""
    results = session.query(Measurement.tobs).\
        filter(Measurement.date > '2017-01-01').all()

    # Convert list of tuples into normal list
    tobs_list = results

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def min_avg_max_start(start):
    """Return the min, avg and max temperatures for a given <start> date."""
    # Calculate the min, avg and max temperatures for a given start date to now.
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # Convert list of tuples into normal list
    min_avg_max_start_list = list(np.ravel(results))

    return jsonify(min_avg_max_start_list)


@app.route("/api/v1.0/<start>/<end>")
def min_avg_max_start_end(start, end):
    """Return the min, avg and max temperatures for a given <start> date to a given <end> date."""
    # Calculate the min, avg and max temperatures for a given start date to a given end date.
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    # Convert list of tuples into normal list
    min_avg_max_start_end_list = list(np.ravel(results))

    return jsonify(min_avg_max_start_end_list)


if __name__ == '__main__':
    app.run()