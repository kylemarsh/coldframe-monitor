from flask import Flask
from flask.ext.restful import Api
from flask.ext.influxdb import InfluxDB

app = Flask(__name__)
app.config.from_pyfile('coldframe.cfg')
api = Api(app)
influx_db = InfluxDB(app)

import coldframe.api
#import coldframe.views
