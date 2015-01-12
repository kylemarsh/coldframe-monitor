from flask import abort, request, render_template
from flask.ext.restful import Resource, reqparse
import requests

from coldframe import app, api, helpers, influx_db


class ReportTempsV0(Resource):
    def post(self):
        """
        v0 of the report_temps resource for the coldframe api.
        Expects the following form data to be submitted:
            token: API authorization token (string)
            series1: value1
            series2: value2
            ...
            seriesN: valueN
        """

        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True, choices=app.config['ACCESS_TOKENS'])
        parser.add_argument('top', type=float)
        parser.add_argument('bottom', type=float)
        parser.add_argument('ambient', type=float)
        args = parser.parse_args()
        del args['token']

        series = []
        for key, value in args.iteritems():
            series.append({
                'name'    : 'coldframe.%s.temp_c' % key,
                'columns' : ['value'],
                'points'  : [[value]]
                })

        wu_data = get_wunderground_data()
        observation_epoch = float(wu_data.pop('observation_epoch'))
        for key, value in wu_data.iteritems():
            series.append({
                'name'    : 'pws.%s.%s' % (app.config['WEATHER_STATION'], key),
                'columns' : ['time', 'value'],
                'points'  : [[observation_epoch, value]]
                })
        dbconn = influx_db.connection
        try:
            result = dbconn.write_points(series)
        except Exception as e:
            import pdb; pdb.set_trace()
            raise e

        return result

api.add_resource(ReportTempsV0, "/api/v0/report_temps")

def get_wunderground_data():
    endpoint = "http://api.wunderground.com/api"
    query = "conditions/q/pws:%s.json" % app.config['WEATHER_STATION']
    key = app.config['WUNDERGROUND_KEY']
    resp = requests.get('/'.join([endpoint, key, query]))
    data = resp.json()['current_observation']
    interesting_data = ['observation_epoch', 'weather', 'temp_c',
            'dewpoint_c', 'precip_today_in', 'pressure_mb',
            'relative_humidity', 'solarradiation', 'wind_degrees', 'wind_kph',
            'wind_gust_kph', 'wind_string', 'windchill_c']
    return {k: data[k] for k in interesting_data}
