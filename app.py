import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np

# creating classes and engine

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
base = automap_base()
base.prepare(engine, reflect=True)

Station = base.classes.station
Measure = base.classes.measurement


from flask import Flask, render_template, jsonify

# creating flask app

app = Flask(__name__)

@app.route("/")
def home():
    print("homepage accessed")
    return render_template('home.html')

@app.route("/api/v1.0/precipitation")
def prcp():
    # initiates session and finds last twelve months of precipitation data, then returns json object
    session = Session(engine)
    last_twelve = session.query(Measure.date, Measure.prcp).filter(Measure.date > '2016-08-22').all()
    session.close()
    last_twelve = dict(last_twelve)
    return jsonify(last_twelve)

@app.route("/api/v1.0/stations")
def stations():
    # initiates session and finds all unique stations in the dataset, then returns json object
    session = Session(engine)
    sts = session.query(Station.station, Station.name).all()
    session.close()
    sts = dict(sts)
    return jsonify(sts)
    
@app.route("/api/v1.0/tobs")
def tobs_j():
    # initiates session and finds last twelve months of temperature observation data for the 
    # most active station, then returns json object
    session = Session(engine)
    _stations = session.query(Measure.station, func.count(Measure.station)).group_by(
    Measure.station).order_by(func.count(Measure.station).desc()).all()
    most_act = _stations[0][0]
    t_obs = session.query(Measure.tobs).filter(
    Measure.station == most_act).filter(
    Measure.date > '2016-08-22').all() 
    session.close()
    d = {most_act : list(t_obs)}
    return jsonify(d)
    
@app.route("/api/v1.0/<start>")
def start(start):
    # initiates session and finds min, max, and average temperature observation (across all stations)
    # since the given start date, and returns json object
    session = Session(engine)
    results = session.query(func.min(Measure.tobs), func.max(Measure.tobs), func.avg(Measure.tobs)).filter(
                Measure.date >= start).all()
    session.close()
    d = {
        f"data after {start}" : {
            'min' : results[0][0],
            'max' : results[0][1],
            'mean' : results[0][2]
        }
    }
    return jsonify(d)
    
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # initiates session and finds min, max, and average temperature observation (across all stations)
    # between the given start and end dates, and returns json object
    session = Session(engine)
    results = session.query(func.min(Measure.tobs), func.max(Measure.tobs), func.avg(Measure.tobs)).filter(
                Measure.date >= start).filter(Measure.date <= end).all()
    session.close()
    d = {
        f"data between {start} and {end}" : {
            'min' : results[0][0],
            'max' : results[0][1],
            'mean' : results[0][2]
        }
    }
    return jsonify(d)


if __name__ == '__main__':
    app.run()

