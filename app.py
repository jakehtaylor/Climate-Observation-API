import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

base = automap_base()
base.prepare(engine, reflect=True)

Station = base.classes.station
Measure = base.classes.measurement

from flask import Flask, render_template, jsonify
app = Flask(__name__)

@app.route("/")
def home():
    print("homepage accessed")
    return render_template('home.html')

@app.route("/api/v1.0/precipitation/pretty")
def prcp_p():
    session = Session(engine)
    last_twelve = session.query(Measure.date, Measure.prcp).filter(Measure.date > '2016-08-22').all()
    session.close()
    last_twelve = dict(last_twelve)
    return render_template('prcp.html', _data_ = (last_twelve))

@app.route("/api/v1.0/precipitation/json")
def prcp_j():
    session = Session(engine)
    last_twelve = session.query(Measure.date, Measure.prcp).filter(Measure.date > '2016-08-22').all()
    session.close()
    last_twelve = dict(last_twelve)
    return jsonify(last_twelve)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    sts = session.query(Station.station, Station.name).all()
    session.close()
    sts = dict(sts)
    return jsonify(sts)
    

@app.route("/api/v1.0/tobs/pretty")
def tobs_p():
    session = Session(engine)
    _stations = session.query(Measure.station, func.count(Measure.station)).group_by(
    Measure.station).order_by(func.count(Measure.station).desc()).all()
    most_act = _stations[0][0]
    t_obs = session.query(Measure.tobs).filter(
    Measure.station == most_act).filter(
    Measure.date > '2016-08-22').all() 
    session.close()
    d = {most_act : list(t_obs)}
    return render_template('tobs.html', _data_=(d))


@app.route("/api/v1.0/tobs/json")
def tobs_j():
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

