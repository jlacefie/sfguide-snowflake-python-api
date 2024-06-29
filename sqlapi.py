import config
import requests
import uuid
from datetime import timedelta
from flask import Blueprint, request

from api_auth import JWTGenerator
from utils import api_response, phone_params_valid, okey_params_valid


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

@sqlapi.route("/sqlapi/customer/details_by_phone")
@api_response
def get_customers_by_phone():
    phone = request.args.get('phone')
    if phone and phone_params_valid(phone):
        sql = f"SELECT C.C_NAME,C.C_ACCTBAL,C.C_ADDRESS,N.N_NAME,R.R_NAME,C_PHONE,C_MKTSEGMENT FROM CUSTOMER C INNER JOIN NATION N ON C.C_NATIONKEY = N.N_NATIONKEY INNER JOIN REGION R ON N.N_REGIONKEY = R.R_REGIONKEY WHERE C.C_PHONE = '{phone}' ORDER BY C.C_NAME;"
        return exec_and_fetch(sql)
    sql = "SELECT COUNT(*) FROM CUSTOMER ;"
    return exec_and_fetch(sql)

@sqlapi.route("/sqlapi/order/orders_by_cust_phone")
@api_response
def get_orders_by_cust_phone():
    phone = request.args.get('phone')
    if phone and phone_params_valid(phone):
        sql = f"SELECT O.O_ORDERKEY, O.O_CUSTKEY, O.O_ORDERSTATUS, O.O_TOTALPRICE, O.O_CLERK FROM ORDERS O INNER JOIN CUSTOMER C ON O.O_CUSTKEY = C.C_CUSTKEY WHERE C.C_PHONE = '{phone}' ORDER BY O_ORDERDATE"
        return exec_and_fetch(sql)
    sql = "SELECT COUNT(*) FROM ORDERS ;"
    return exec_and_fetch(sql)

@sqlapi.route("/sqlapi/order/details_by_orderkey")
@api_response
def get_orders_details_by_okey():
    okey = request.args.get('okey')
    if okey and okey_params_valid(okey):
        sql = f"SELECT O.O_ORDERKEY, O.O_CUSTKEY, O.O_ORDERSTATUS, O.O_TOTALPRICE, O.O_CLERK, L.L_LINENUMBER, L.L_LINESTATUS, L.L_QUANTITY, L.L_EXTENDEDPRICE, L.L_TAX, L.L_SHIPDATE, L.L_SHIPINSTRUCT, L.L_SHIPMODE, L.L_RETURNFLAG, P.P_NAME, P.P_BRAND, P.P_MFGR, P.P_SIZE, P.P_TYPE FROM ORDERS O INNER JOIN CUSTOMER C ON O.O_CUSTKEY = C.C_CUSTKEY INNER JOIN LINEITEM L ON O.O_ORDERKEY = L.L_ORDERKEY INNER JOIN PART P ON L.L_PARTKEY = P.P_PARTKEY WHERE O.O_ORDERKEY = '{okey}' ORDER BY O.O_ORDERDATE, L.L_LINENUMBER"
        return exec_and_fetch(sql)
    sql = "SELECT COUNT(*) FROM ORDERS ;"
    return exec_and_fetch(sql)