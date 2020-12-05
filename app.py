from flask import Flask, jsonify
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy as db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

#PLEASE GRADE. CHANGE THE file_path TO Resources/hawaii.sqlite TO MAKE THE CODE RUN. 
file_path = "/Users/ulissesmiranda/Documents/GitHub/sqlalchemy-challenge/Resources/hawaii.sqlite"
engine = create_engine(f'sqlite:////{file_path}', echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)

#Creating classes
print(Base.classes.keys())
Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)

#display all available routes
@app.route("/")
def home():
    return (
        f"Welcome to the SQL-Alchemy APP API!<br/>"
        f"Available Routes:<br/>"
        f"------------------------------------------<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/                 [enter start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/                 [enter start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
        f"------------------------------------------<br/>"
    )

# Create route to return precipitations
@app.route("/api/v1.0/precipitation")
def Precipitation():
    session = Session(engine)
    last_date=dt.date(2017, 8, 23)
    prev_year=last_date-dt.timedelta(days=365)
    results=session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date>=prev_year, Measurement.date<=last_date).\
                order_by(Measurement.date.desc()).all()
    session.close()
    
# for loop to create a dictionary
    all_Precipitation = []
    for date, prcp in results:
        Precipitation_dict = {}
        Precipitation_dict['date'] = date
        Precipitation_dict['prcp'] = prcp
        all_Precipitation.append(Precipitation_dict)
    return jsonify(all_Precipitation)

#Create a route to display all stations
@app.route("/api/v1.0/stations")
def Stations():
    session = Session(engine)
    active_st = session.query(Station.station, Station.name).all()
    session.close()
#loop to create dictionary
    all_Station = []
    for station, name in active_st:
        Station_dict = {}
        Station_dict['station'] = station
        Station_dict['name'] = name
        all_Station.append(Station_dict)
    return jsonify(all_Station)

    
#route for Temperatures
@app.route("/api/v1.0/tobs")
def Temperatures():
    session = Session(engine)

    last_date=dt.date(2017, 8, 23)
    prev_year=last_date-dt.timedelta(days=365)


    results_2=session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.station == 'USC00519281',\
                       Measurement.date>=prev_year,\
                       Measurement.date<=last_date).all()
    session.close()

   

    all_Temperatures = []
    for date, tobs in results_2:
        Temperatures_dict = {}
        Temperatures_dict['date'] = date
        Temperatures_dict['tobs'] = tobs
        all_Temperatures.append(Temperatures_dict)
    
    return jsonify(all_Temperatures)

#Route to return temperatures from a given date to the end of the dataset
@app.route('/api/v1.0/<start>')
def get_t_start(start):
    session = Session(engine)
    queryresult = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).group_by(Measurement.date).all()
    session.close()

    
    tobsall = []
    for min,avg,max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)

    np.ravel(tobsall)
    return jsonify(tobsall)

#Route to return the temperatures from a given start date to a given end date 
@app.route('/api/v1.0/<start>/<end_date>')
def get_start_end(start, end_date):
    session = Session(engine)
    queryresult_2 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end_date).group_by(Measurement.date).all()
    session.close()

    
    tobsall = []
    for min,avg,max in queryresult_2:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)

    np.ravel(tobsall)
    return jsonify(tobsall)


 
 
if __name__ == '__main__':
    app.run(debug=True)