import config
import requests
import uuid
from datetime import timedelta
from flask import Blueprint, request

from api_auth import JWTGenerator
from utils import api_response, phone_params_valid


sqlapi = Blueprint('sqlapi', __name__)
authfn = JWTGenerator(config.SNOWFLAKE_ACCOUNT, config.SNOWFLAKE_USER, config.SNOWFLAKE_PRIVATE_KEY, timedelta(59), timedelta(54)).get_token
http_session = requests.Session()
url_base = f"https://{config.SNOWFLAKE_ACCOUNT}.snowflakecomputing.com"

HEADERS = {
    "Authorization": "Bearer " + authfn(),
    "Content-Type": "application/json",
    "Snowflake-Account": config.SNOWFLAKE_ACCOUNT,
    "Accept": "application/json",
    "X-Snowflake-Authorization-Token-Type": "KEYPAIR_JWT"
}


def sql2body(sql):
    result = {
        "statement": f"{sql}",
        "timeout": 60,
        "resultSetMetaData": {
            "format": "json"
        },
        "database": config.SNOWFLAKE_DATABASE,
        "schema": config.SNOWFLAKE_SCHEMA,
        "warehouse": config.SNOWFLAKE_WAREHOUSE,
        "parameters": {"query_tag": "Snowflake-Python-SQLApi"},
        }
    return result


def exec_and_fetch(sql):
    jsonBody = sql2body(sql)
    r = http_session.post(f"{url_base}/api/v2/statements?requestId={str(uuid.uuid4())}&retry=true", json=jsonBody, headers=HEADERS)
    if r.status_code == 200:
        result = r.json()['data']
        return result
    else:
        print(f"ERROR: Status code from {sql}: {r.status_code}")
        raise Exception("Invalid response from API")


@sqlapi.route("/sqlapi/customer/detais_by_phone")
@api_response
def get_customers_by_phone():
    phone = request.args.get('phone')
    if phone and phone_params_valid(phone):
        sql = f"SELECT C.C_NAME AS Name,C.C_ACCTBAL AS Account_Balance,C.C_ADDRESS AS Address,N.N_NAME AS Nation,R.R_NAME AS Region,C_PHONE AS Phone,C_MKTSEGMENT AS Market_Segment FROM CUSTOMER C INNER JOIN NATION N ON C.C_NATIONKEY = N.N_NATIONKEY INNER JOIN REGION R ON N.N_REGIONKEY = R.R_REGIONKEY WHERE C.C_PHONE'{phone}'ORDER BY C.C_NAME;"
        return exec_and_fetch(sql)
    sql = "SELECT COUNT(*) FROM CUSTOMER ;"
    return exec_and_fetch(sql)