import config
import snowflake.connector
from flask import Blueprint, request

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from utils import api_response


def connect():
    p_key = serialization.load_pem_private_key(
            config.SNOWFLAKE_PRIVATE_KEY.encode('utf-8'),
            password=None,
            backend=default_backend()
        )
    pkb = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())

    snowflake.connector.paramstyle='qmark'
    conn = snowflake.connector.connect(
        user=config.SNOWFLAKE_USER,
        account=config.SNOWFLAKE_ACCOUNT,
        warehouse=config.SNOWFLAKE_WAREHOUSE,
        schema=config.SNOWFLAKE_SCHEMA,
        database=config.SNOWFLAKE_DATABASE,
        private_key=pkb,
        session_parameters={
            'QUERY_TAG': 'Snowflake-Python-Api',
        })
   
    return conn


conn = connect()
connector = Blueprint('connector', __name__)


def exec_and_fetch(sql, params = None):
    cur = conn.cursor().execute(sql, params)
    return cur.fetchall()


@connector.route("/trips/monthly")
@api_response
def get_trips_monthly():
    start_range = request.args.get('start_range')
    end_range = request.args.get('end_range')
    if start_range and end_range:
        sql = "select COUNT(*) as trip_count, MONTHNAME(starttime) as month from demo.trips where starttime between ? and ? group by MONTH(starttime), MONTHNAME(starttime) order by MONTH(starttime);"
        return exec_and_fetch(sql, (start_range, end_range))
    sql = "select COUNT(*) as trip_count, MONTHNAME(starttime) as month from demo.trips group by MONTH(starttime), MONTHNAME(starttime) order by MONTH(starttime);"
    return exec_and_fetch(sql)


@connector.route("/trips/day_of_week")
@api_response
def get_day_of_week():
    start_range = request.args.get('start_range')
    end_range = request.args.get('end_range')
    if start_range and end_range:
        sql = "select COUNT(*) as trip_count, DAYNAME(starttime) as day_of_week from demo.trips where starttime between ? and ? group by DAYOFWEEK(starttime), DAYNAME(starttime) order by DAYOFWEEK(starttime);"
        return exec_and_fetch(sql, (start_range, end_range))
    sql = "select COUNT(*) as trip_count, DAYNAME(starttime) as day_of_week from demo.trips group by DAYOFWEEK(starttime), DAYNAME(starttime) order by DAYOFWEEK(starttime);"
    return exec_and_fetch(sql)


@connector.route("/trips/temperature")
@api_response
def get_temperature():
    start_range = request.args.get('start_range')
    end_range = request.args.get('end_range')
    if start_range and end_range:
        sql = "with weather_trips as (select * from demo.trips t inner join demo.weather w on date_trunc(\"day\", t.starttime) = w.observation_date) select round(temp_avg_f, -1) as temp, count(*) as trip_count from weather_trips where starttime between ? and ? group by round(temp_avg_f, -1) order by round(temp_avg_f, -1) asc;"
        return exec_and_fetch(sql, (start_range, end_range))
    sql = "with weather_trips as (select * from demo.trips t inner join demo.weather w on date_trunc(\"day\", t.starttime) = w.observation_date) select round(temp_avg_f, -1) as temp, count(*) as trip_count from weather_trips group by round(temp_avg_f, -1) order by round(temp_avg_f, -1) asc;"
    return exec_and_fetch(sql)