import config
import snowflake.connector
from flask import Blueprint, request

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from utils import api_response, phone_params_valid


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
            'QUERY_TAG': 'Snowflake-Python-Connector',
        })
   
    return conn


conn = connect()
connector = Blueprint('connector', __name__)


def exec_and_fetch(sql, params = None):
    cur = conn.cursor().execute(sql, params)
    return cur.fetchall()


@connector.route("/customer/detais_by_phone")
@api_response
def get_customers_by_phone():
    phone = request.args.get('phone')
    if phone and phone_params_valid(phone):
        sql = f"SELECT C.C_NAME AS Name,C.C_ACCTBAL AS Account_Balance,C.C_ADDRESS AS Address,N.N_NAME AS Nation,R.R_NAME AS Region,C_PHONE AS Phone,C_MKTSEGMENT AS Market_Segment FROM CUSTOMER C INNER JOIN NATION N ON C.C_NATIONKEY = N.N_NATIONKEY INNER JOIN REGION R ON N.N_REGIONKEY = R.R_REGIONKEY WHERE C.C_PHONE'{phone}'ORDER BY C.C_NAME;"
        return exec_and_fetch(sql)
    sql = "SELECT COUNT(*) FROM CUSTOMER ;"
    return exec_and_fetch(sql)