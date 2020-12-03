from flask import Flask
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

file_path = "hawaii.sqlite"
engine = create_engine(f'sqlite:///{file_path}', echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return (
           "available routes"\
           "Precipitation"\
           "Stations"\
           "Temperatures Observed"\
           "<start>"\
           "<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def Precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp)
    session.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)